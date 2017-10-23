from datetime import date, datetime
import datacube
from datacube_wms.wms_cfg import service_cfg, layer_cfg
from psycopg2.extras import Json

def accum_min(a, b):
    if a is None:
        return b
    elif b is None:
        return a
    else:
        return min(a,b)


def accum_max(a, b):
    if a is None:
        return b
    elif b is None:
        return a
    else:
        return max(a,b)


def determine_product_ranges(dc, product_name):
    product = dc.index.products.get_by_name(product_name)
    r = {
        "product_id": product.id,

        "lat": {
            "min": None,
            "max": None
        },
        "lon": {
            "min": None,
            "max": None
        },
    }
    time_set = set()

    crsids = service_cfg["published_CRSs"]
    extents = { crsid: None for crsid in crsids }
    crses = { crsid: datacube.utils.geometry.CRS(crsid) for crsid in crsids }

    for ds in dc.find_datasets(product=product_name):
        r["lat"]["min"] = accum_min(r["lat"]["min"], ds.metadata.lat.begin)
        r["lat"]["max"] = accum_max(r["lat"]["max"], ds.metadata.lat.end)
        r["lon"]["min"] = accum_min(r["lon"]["min"], ds.metadata.lon.begin)
        r["lon"]["max"] = accum_max(r["lon"]["max"], ds.metadata.lon.end)

        time_set.add(ds.center_time.date())

        for crsid in crsids:
            crs = crses[crsid]
            ext = ds.extent
            if ext.crs != crs:
                ext = ext.to_crs(crs)
            if extents[crsid] is None:
                extents[crsid] = ext
            else:
                extents[crsid] = extents[crsid].union(ext)

    r["times"] = sorted(time_set)
    r["bboxes"] = { crsid: extents[crsid].boundingbox for crsid in crsids }
    return r


def determine_ranges(dc):
    ranges = []
    for layer in layer_cfg:
        for product_cfg in layer["products"]:
            ranges.append(determine_product_ranges(dc, product_cfg["name"]))
    return ranges


def get_sqlconn(dc):
    # TODO: Is this the really the best way to obtain an SQL connection?
    return dc.index._db._engine.connect()


def get_ids_in_db(conn):
    results = conn.execute("select id from wms.product_ranges")
    return [ r["id"] for r in results ]


def rng_update(conn, rng):
    conn.execute("""
            UPDATE wms.product_ranges
            SET
                  lat_min=%s,
                  lat_max=%s,
                  lon_min=%s,
                  lon_max=%s,   
                  dates=%s,
                  bboxes=%s
            WHERE id=%s
    """,
                 rng["lat"]["min"],
                 rng["lat"]["max"],
                 rng["lon"]["min"],
                 rng["lon"]["max"],

                 Json([ t.strftime("%Y-%m-%d")  for t in rng["times"] ]),
                 Json({ crsid: {"top": bbox.top, "bottom": bbox.bottom, "left": bbox.left, "right": bbox.right}
                        for crsid, bbox in rng["bboxes"].items()
                        }),

                 rng["product_id"],
                 )


def rng_insert(conn, rng):
    conn.execute("""
            INSERT into wms.product_ranges
                (id,   lat_min,lat_max,lon_min,lon_max,   dates,bboxes)
            VALUES
                (%s,   %s,%s,%s,%s,    %s,%s)
    """,
                 rng["product_id"],

                 rng["lat"]["min"],
                 rng["lat"]["max"],
                 rng["lon"]["min"],
                 rng["lon"]["max"],

                 Json([ t.strftime("%Y-%m-%d")  for t in rng["times"] ]),
                 Json({ crsid: {"top": bbox.top, "bottom": bbox.bottom, "left": bbox.left, "right": bbox.right}
                            for crsid, bbox in rng["bboxes"].items()
                     })
                 )


def update_all_ranges(dc):
    ranges = determine_ranges(dc)
    conn = get_sqlconn(dc)
    txn = conn.begin()
    ids_in_db = get_ids_in_db(conn)
    i = 0
    u = 0
    for prod_ranges in ranges:
        if prod_ranges["product_id"] in ids_in_db:
            rng_update(conn, prod_ranges)
            u += 1
        else:
            rng_insert(conn, prod_ranges)
            i += 1
    txn.commit()
    conn.close()
    return u, i

def get_ranges(dc, product):
    if isinstance(product, str):
        product = dc.index.products.get_by_name(product)
    conn = get_sqlconn(dc)
    results = conn.execute("select * from wms.product_ranges where id=%s", product.id)
    for result in results:
        conn.close()
        times = [ datetime.strptime(d, "%Y-%m-%d").date() for d in result["dates"]]
        return {
            "lat": {
                "min": result["lat_min"],
                "max": result["lat_max"],
            },
            "lon": {
                "min": result["lon_min"],
                "max": result["lon_max"],
            },
            "times": times,
            "time_set": set(times),
            "bboxes": result["bboxes"]
        }