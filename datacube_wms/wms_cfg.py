# Static config for the wms metadata.
import os

response_cfg = {
    "Access-Control-Allow-Origin": "*",   # CORS header
}

service_cfg = {
    # Required config
    "title": "WMS server for Australian Landsat Datacube",
    "url": os.environ.get("PUBLIC_URL", "http://localhost:5000/"),
    "published_CRSs": {
        "EPSG:3857": { # Web Mercator
            "geographic": False,
            "horizontal_coord": "x",
            "vertical_coord": "y",
        },
        "EPSG:4326": { # WGS-84
            "geographic": True,
        },
        "EPSG:3577": { # GDA-94, internal representation
            "geographic": False,
            "horizontal_coord": "easting",
            "vertical_coord": "northing",
        },
    },
    
    # Technically optional config, but strongly recommended
    "layer_limit": 1,
    "max_width": 512,
    "max_height": 512,

    # Optional config - may be set to blank/empty
    "abstract": """Historic Landsat imagery for Australia.""",
    "keywords": [
        "landsat",
        "australia",
        "time-series",
    ],
    "contact_info": {
        "person": "David Gavin",
        "organisation": "Geoscience Australia",
        "position": "Technical Lead",
        "address": {
            "type": "postal",
            "address": "GPO Box 378",
            "city": "Canberra",
            "state": "ACT",
            "postcode": "2906",
            "country": "Australia",
        },
        "telephone": "+61 2 1234 5678",
        "fax": "+61 2 1234 6789",
        "email": "test@example.com",
    },
    "fees": "",
    "access_constraints": "",
}

layer_cfg = [
    # Layer Config is a list of platform configs
    {
        # Name and title of the platform layer.
        # Platform layers are not mappable. The name is for internal server use only.
        "name": "LANDSAT_8",
        "title": "Landsat 8",
        "abstract": "Images from the Landsat 8 satellite",

        # Products available for this platform.
        # For each product, the "name" is the Datacube name, and the label is used
        # to describe the label to end-users.
        "products": [
            {
                # Included as a keyword  for the layer
                "label": "NBAR-T",
                # Included as a keyword  for the layer
                "type": "surface reflectance",
                # Included as a keyword  for the layer
                "variant": "terrain corrected",
                # The WMS name for the layer
                "name": "ls8_nbart_albers",
                # The Datacube name for the associated data product
                "product_name": "ls8_nbart_albers",
                # The Datacube name for the associated pixel-quality product (optional)
                # The name of the associated Datacube pixel-quality product
                "pq_dataset": "ls8_pq_albers",
                # The name of the measurement band for the pixel-quality product
                # (Only required if pq_dataset is set)
                "pq_band": "pixelquality",
                # Min zoom factor - sets the zoom level where the cutover from indicative polygons
                # to actual imagery occurs.
                "min_zoom_factor": 500.0,
                # The fill-colour of the indicative polygons when zoomed out.
                # Triplets (rgb) or quadruplets (rgba) of integers 0-255.
                "zoomed_out_fill_colour": [ 150, 180, 200, 160],
                # Time Zone.  In hours added to UTC (maybe negative)
                # Used for rounding off scene times to a date.
                # 9 is good value for imagery of Australia.
                "time_zone": 9
            },
            {
                # Included as a keyword  for the layer
                "label": "FC",
                # Included as a keyword  for the layer
                "type": "fractional cover",
                # Included as a keyword  for the layer
                "variant": "terrain corrected",
                # The WMS name for the layer
                "name": "ls8_fc_albers",
                # The Datacube name for the associated data product
                "product_name": "ls8_fc_albers",
                # The Datacube name for the associated pixel-quality product (optional)
                # The name of the associated Datacube pixel-quality product
                "pq_dataset": "ls8_pq_albers",
                # The name of the measurement band for the pixel-quality product
                # (Only required if pq_dataset is set)
                "pq_band": "pixelquality",
                # Min zoom factor - sets the zoom level where the cutover from indicative polygons
                # to actual imagery occurs.
                "min_zoom_factor": 500.0,
                # The fill-colour of the indicative polygons when zoomed out.
                # Triplets (rgb) or quadruplets (rgba) of integers 0-255.
                "zoomed_out_fill_colour": [ 150, 180, 200, 160],
                # Time Zone.  In hours added to UTC (maybe negative)
                # Used for rounding off scene times to a date.
                # 9 is good value for imagery of Australia.
                "time_zone": 9
            },
        ],
        # Styles.
        #
        # See band_mapper.py
        #
        # The various available spectral bands, and ways to combine them
        # into a single rgb image.
        # The examples here are ad hoc
        #
        # LS7:  http://www.indexdatabase.de/db/s-single.php?id=8
        # LS8:  http://www.indexdatabase.de/db/s-single.php?id=168
        "styles": [
            # Examples of styles which are linear combinations of the available spectral bands.
            #
            {
                "name": "simple_rgb",
                "title": "Simple RGB",
                "abstract": "Simple true-colour image, using the red, green and blue bands",
                "components": {
                    "red": {
                        "red": 1.0
                    },
                    "green": {
                        "green": 1.0
                    },
                    "blue": {
                        "blue": 1.0
                    }
                },
                # Used to clip off very bright areas.
                "scale_factor": 12.0
            },
            {
                "name": "cloud_masked_rgb",
                "title": "Simple RGB with cloud masking",
                "abstract": "Simple true-colour image, using the red, green and blue bands, with cloud masking",
                "components": {
                    "red": {
                        "red": 1.0
                    },
                    "green": {
                        "green": 1.0
                    },
                    "blue": {
                        "blue": 1.0
                    }
                },
                # PQ masking example
                "pq_mask_flags": {
                    "cloud_acca": "no_cloud",
                    "cloud_fmask": "no_cloud",
                },
                "scale_factor": 12.0
            },
            {
                "name": "extended_rgb",
                "title": "Extended RGB",
                "abstract": "Extended true-colour image, incorporating the coastal aerosol band",
                "components": {
                    "red": {
                        "red": 1.0
                    },
                    "green": {
                        "green": 1.0
                    },
                    "blue": {
                        "blue": 0.6,
                        "coastal_aerosol": 0.4
                    }
                },
                "scale_factor": 12.0
            },
            {
                "name": "wideband",
                "title": "Wideband false-colour",
                "abstract": "False-colour image, incorporating all available spectral bands",
                "components": {
                    "red": {
                        "swir2": 0.255,
                        "swir1": 0.45,
                        "nir": 0.255,
                    },
                    "green": {
                        "nir": 0.255,
                        "red": 0.45,
                        "green": 0.255,
                    },
                    "blue": {
                        "green": 0.255,
                        "blue": 0.45,
                        "coastal_aerosol": 0.255,
                    }
                },
                "scale_factor": 12.0
            },
            {
                "name": "infra_red",
                "title": "False colour multi-band infra-red",
                "abstract": "Simple false-colour image, using the near and short-wave infra-red bands",
                "components": {
                    "red": {
                        "swir1": 1.0
                    },
                    "green": {
                        "swir2": 1.0
                    },
                    "blue": {
                        "nir": 1.0
                    }
                },
                "scale_factor": 12.0
            },
            {
                "name": "coastal_aerosol",
                "title": "Spectral band 1 - Coastal aerosol",
                "abstract": "Coastal aerosol band, approximately 435nm to 450nm",
                "components": {
                    "red": {
                        "coastal_aerosol": 1.0
                    },
                    "green": {
                        "coastal_aerosol": 1.0
                    },
                    "blue": {
                        "coastal_aerosol": 1.0
                    }
                },
                "scale_factor": 12.0
            },
            {
                "name": "blue",
                "title": "Spectral band 2 - Blue",
                "abstract": "Blue band, approximately 453nm to 511nm",
                "components": {
                    "red": {
                        "blue": 1.0
                    },
                    "green": {
                        "blue": 1.0
                    },
                    "blue": {
                        "blue": 1.0
                    }
                },
                "scale_factor": 12.0
            },
            {
                "name": "green",
                "title": "Spectral band 3 - Green",
                "abstract": "Green band, approximately 534nm to 588nm",
                "components": {
                    "red": {
                        "green": 1.0
                    },
                    "green": {
                        "green": 1.0
                    },
                    "blue": {
                        "green": 1.0
                    }
                },
                "scale_factor": 12.0
            },
            {
                "name": "red",
                "title": "Spectral band 4 - Red",
                "abstract": "Red band, roughly 637nm to 672nm",
                "components": {
                    "red": {
                        "red": 1.0
                    },
                    "green": {
                        "red": 1.0
                    },
                    "blue": {
                        "red": 1.0
                    }
                },
                "scale_factor": 12.0
            },
            {
                "name": "nir",
                "title": "Spectral band 5 - Near infra-red",
                "abstract": "Near infra-red band, roughly 853nm to 876nm",
                "components": {
                    "red": {
                        "nir": 1.0
                    },
                    "green": {
                        "nir": 1.0
                    },
                    "blue": {
                        "nir": 1.0
                    }
                },
                "scale_factor": 12.0
            },
            {
                "name": "swir1",
                "title": "Spectral band 6 - Short wave infra-red 1",
                "abstract": "Short wave infra-red band 1, roughly 1575nm to 1647nm",
                "components": {
                    "red": {
                        "swir1": 1.0
                    },
                    "green": {
                        "swir1": 1.0
                    },
                    "blue": {
                        "swir1": 1.0
                    }
                },
                "scale_factor": 12.0
            },
            {
                "name": "swir2",
                "title": "Spectral band 7 - Short wave infra-red 2",
                "abstract": "Short wave infra-red band 2, roughly 2117nm to 2285nm",
                "components": {
                    "red": {
                        "swir2": 1.0
                    },
                    "green": {
                        "swir2": 1.0
                    },
                    "blue": {
                        "swir2": 1.0
                    }
                },
                "scale_factor": 12.0
            },
            #
            # Examples of FC styles.
            {
                "name": "simple_fc",
                "title": "Fractional Cover",
                "abstract": "Fractional cover representation, with green vegetation in green, dead vegetation in blue, and bare soil in red",
                "components": {
                    "red": {
                        "BS": 1.0
                    },
                    "green": {
                        "PV": 1.0
                    },
                    "blue": {
                        "NPV": 1.0
                    }
                },
                # Used to clip off very bright areas.
                "scale_factor": 0.39
            },
            {
                "name": "fc_cloudmask",
                "title": "Fractional Cover (Cloud masked)",
                "abstract": "Fractional cover representation, with green vegetation in green, dead vegetation in blue, and bare soil in red",
                "needed_bands": ["BS", "PV", "NPV"],
                # Areas where the index_function returns outside the range are masked.
                "range": [0.0, 1.0],
                "components": {
                    "red": {
                        "BS": 1.0
                    },
                    "green": {
                        "PV": 1.0
                    },
                    "blue": {
                        "NPV": 1.0
                    }
                },
                "pq_mask_flags": {
                    "cloud_acca": "no_cloud",
                    "cloud_fmask": "no_cloud",
                },
                "scale_factor": 0.39
            },
            #
            # Examples of non-linear heat-mapped styles.
            {
                "name": "ndvi",
                "title": "NDVI",
                "abstract": "Normalised Difference Vegetation Index - a derived index that correlates well with the existence of vegetation",
                "heat_mapped": True,
                "index_function": lambda data: (data["nir"] - data["red"]) / (data["nir"] + data["red"]),
                "needed_bands": [ "red", "nir" ],
                # Areas where the index_function returns outside the range are masked.
                "range": [ 0.0, 1.0 ],
            },
            {
                "name": "ndvi_cloudmask",
                "title": "NDVI with cloud masking",
                "abstract": "Normalised Difference Vegetation Index (with cloud masking) - a derived index that correlates well with the existence of vegetation",
                "heat_mapped": True,
                "index_function": lambda data: (data["nir"] - data["red"]) / (data["nir"] + data["red"]),
                "needed_bands": [ "red", "nir" ],
                # Areas where the index_function returns outside the range are masked.
                "range": [ 0.0, 1.0 ],
                "pq_mask_flags": {
                    "cloud_acca": "no_cloud",
                    "cloud_fmask": "no_cloud",
                },
            },
            {
                "name": "ndwi",
                "title": "NDWI",
                "abstract": "Normalised Difference Water Index - a derived index that correlates well with the existence of water",
                "heat_mapped": True,
                "index_function": lambda data: (data["green"] - data["nir"]) / (data["nir"] + data["green"]),
                "needed_bands": [ "green", "nir" ],
                "range": [ 0.0, 1.0 ],
            },
            {
                "name": "ndbi",
                "title": "NDBI",
                "abstract": "Normalised Difference Buildup Index - a derived index that correlates with the existence of urbanisation",
                "heat_mapped": True,
                "index_function": lambda data: (data["swir2"] - data["nir"]) / (data["swir2"] + data["nir"]),
                "needed_bands": [ "swir2", "nir" ],
                "range": [ 0.0, 1.0 ],
            },
            # Mask layers - examples of how to display raw pixel quality data.
            # This works by creatively mis-using the Heatmap style class.
            {
                "name": "cloud_mask",
                "title": "Cloud Mask",
                "abstract": "Highlight pixels without cloud.",
                "heat_mapped": True,
                "index_function": lambda data: data["red"] * 0.0 + 0.1,
                "needed_bands": [ "red" ],
                "range": [ 0.0, 1.0 ],
                # Mask flags normally describe which areas SHOULD be shown.
                # (i.e. pixels for which any of the declared flags are true)
                # pq_mask_invert is intended to invert this logic.
                # (i.e. pixels for which none of the declared flags are true)
                #
                # i.e. Specifying like this shows pixels which not clouds in either metric.
                #      Specifying "cloud" and setting the "pq_mask_invert" to False would
                #      show pixels which are not clouds in both metrics.
                "pq_mask_invert": True,
                "pq_mask_flags": {
                    "cloud_acca": "no_cloud",
                    "cloud_fmask": "no_cloud",
                },
            },
            {
                "name": "cloud_acca",
                "title": "Cloud acca Mask",
                "abstract": "Highlight pixels with cloud.",
                "heat_mapped": True,
                "index_function": lambda data: data["red"] * 0.0 + 0.4,
                "needed_bands": [ "red" ],
                "range": [ 0.0, 1.0 ],
                "pq_mask_flags": {
                    "cloud_acca": "cloud",
                },
            },
            {
                "name": "cloud_fmask",
                "title": "Cloud fmask Mask",
                "abstract": "Highlight pixels with cloud.",
                "heat_mapped": True,
                "index_function": lambda data: data["red"] * 0.0 + 0.8,
                "needed_bands": [ "red" ],
                "range": [ 0.0, 1.0 ],
                "pq_mask_flags": {
                    "cloud_fmask": "cloud",
                },
            },
            {
                "name": "contiguous_mask",
                "title": "Contiguous Data Mask",
                "abstract": "Highlight pixels with non-contiguous data",
                "heat_mapped": True,
                "index_function": lambda data: data["red"] * 0.0 + 0.3,
                "needed_bands": [ "red" ],
                "range": [ 0.0, 1.0 ],
                "pq_mask_flags": {
                    "contiguous": False
                },
            },
            # Hybrid style - mixes a linear mapping and a heat mapped index
            {
                "name": "rgb_ndvi",
                "title": "NDVI plus RGB",
                "abstract": "Normalised Difference Vegetation Index (blended with RGB) - a derived index that correlates well with the existence of vegetation",
                "component_ratio": 0.6,
                "heat_mapped": True,
                "index_function": lambda data: (data["nir"] - data["red"]) / (data["nir"] + data["red"]),
                "needed_bands": [ "red", "nir" ],
                # Areas where the index_function returns outside the range are masked.
                "range": [ 0.0, 1.0 ],
                "components": {
                    "red": {
                        "red": 1.0
                    },
                    "green": {
                        "green": 1.0
                    },
                    "blue": {
                        "blue": 1.0
                    }
                },
                "scale_factor": 12.0
            },
            {
                "name": "rgb_ndvi_cloudmask",
                "title": "NDVI plus RGB (Cloud masked)",
                "abstract": "Normalised Difference Vegetation Index (blended with RGB and cloud masked) - a derived index that correlates well with the existence of vegetation",
                "component_ratio": 0.6,
                "heat_mapped": True,
                "index_function": lambda data: (data["nir"] - data["red"]) / (data["nir"] + data["red"]),
                "needed_bands": [ "red", "nir" ],
                # Areas where the index_function returns outside the range are masked.
                "range": [ 0.0, 1.0 ],
                "components": {
                    "red": {
                        "red": 1.0
                    },
                    "green": {
                        "green": 1.0
                    },
                    "blue": {
                        "blue": 1.0
                    }
                },
                "pq_mask_flags": {
                    "cloud_acca": "no_cloud",
                    "cloud_fmask": "no_cloud",
                },
                "scale_factor": 12.0
            },
        ],
        # Default style (if request does not specify style)
        # MUST be defined in the styles list above.

        # (Looks like Terria assumes this is the first style in the list, but this is
        #  not required by the standard.)
        "default_style": "simple_rgb",
    },
]

to_be_added_to_layer_cfg = {
        "name": "LANDSAT_7",
        "title": "Landsat 7",
        "abstract": "Images from the Landsat 7 satellite",

        "products": [
            {
                "label": "NBAR-T",
                "type": "surface reflectance",
                "variant": "terrain corrected",
                "name": "ls7_nbart_albers",
                "product_name": "ls7_nbart_albers",
                "pq_dataset": "ls7_pq_albers",
                "pq_band": "pixelquality",
                "pq_mask_flags": {
                    "contiguous": True
                },
                "min_zoom_factor": 500.0
            },
        ],
        "styles": [
            {
                "name": "simple_rgb",
                "title": "Simple RGB",
                "abstract": "Simple true-colour image, using the red, green and blue bands",
                "components": {
                    "red": {
                        "red": 1.0
                    },
                    "green": {
                        "green": 1.0
                    },
                    "blue": {
                        "blue": 1.0
                    }
                },
                "scale_factor": 12.0
            },
            {
                "name": "wideband",
                "title": "Wideband false-colour",
                "abstract": "False-colour image, incorporating all available spectral bands",
                "components": {
                    "red": {
                        "swir2": 0.5,
                        "swir1": 0.5,
                    },
                    "green": {
                        "nir": 0.5,
                        "red": 0.5,
                    },
                    "blue": {
                        "green": 0.5,
                        "blue": 0.5,
                    }
                },
                "scale_factor": 12.0
            },
            {
                "name": "infra_red",
                "title": "False colour multi-band infra-red",
                "abstract": "Simple false-colour image, using the near and short-wave infra-red bands",
                "components": {
                    "red": {
                        "swir1": 1.0
                    },
                    "green": {
                        "swir2": 1.0
                    },
                    "blue": {
                        "nir": 1.0
                    }
                },
                "scale_factor": 12.0
            },
            {
                "name": "blue",
                "title": "Spectral band 1 - Blue",
                "abstract": "Blue band, approximately 450nm to 520nm",
                "components": {
                    "red": {
                        "blue": 1.0
                    },
                    "green": {
                        "blue": 1.0
                    },
                    "blue": {
                        "blue": 1.0
                    }
                },
                "scale_factor": 12.0
            },
            {
                "name": "green",
                "title": "Spectral band 2 - Green",
                "abstract": "Green band, approximately 530nm to 610nm",
                "components": {
                    "red": {
                        "green": 1.0
                    },
                    "green": {
                        "green": 1.0
                    },
                    "blue": {
                        "green": 1.0
                    }
                },
                "scale_factor": 12.0
            },
            {
                "name": "red",
                "title": "Spectral band 3 - Red",
                "abstract": "Red band, roughly 630nm to 690nm",
                "components": {
                    "red": {
                        "red": 1.0
                    },
                    "green": {
                        "red": 1.0
                    },
                    "blue": {
                        "red": 1.0
                    }
                },
                "scale_factor": 12.0
            },
            {
                "name": "nir",
                "title": "Spectral band 4 - Near infra-red",
                "abstract": "Near infra-red band, roughly 780nm to 840nm",
                "components": {
                    "red": {
                        "nir": 1.0
                    },
                    "green": {
                        "nir": 1.0
                    },
                    "blue": {
                        "nir": 1.0
                    }
                },
                "scale_factor": 12.0
            },
            {
                "name": "swir1",
                "title": "Spectral band 5 - Short wave infra-red 1",
                "abstract": "Short wave infra-red band 1, roughly 1550nm to 1750nm",
                "components": {
                    "red": {
                        "swir1": 1.0
                    },
                    "green": {
                        "swir1": 1.0
                    },
                    "blue": {
                        "swir1": 1.0
                    }
                },
                "scale_factor": 12.0
            },
            {
                "name": "swir2",
                "title": "Spectral band 6 - Short wave infra-red 2",
                "abstract": "Short wave infra-red band 2, roughly 2090nm to 2220nm",
                "components": {
                    "red": {
                        "swir2": 1.0
                    },
                    "green": {
                        "swir2": 1.0
                    },
                    "blue": {
                        "swir2": 1.0
                    }
                },
                "scale_factor": 12.0
            }
        ],
        "default_style": "simple_rgb",
}
