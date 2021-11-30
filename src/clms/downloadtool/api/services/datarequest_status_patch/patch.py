# -*- coding: utf-8 -*-
"""
For HTTP GET operations we can use standard HTTP parameter passing
(through the URL)

"""
import re
from logging import getLogger
import datetime

from plone.restapi.services import Service
from plone.restapi.deserializer import json_body


from zope.component import getUtility
from clms.downloadtool.utility import IDownloadToolUtility

log = getLogger(__name__)

countries = {
    "BD": "BGD",
    "BE": "BEL",
    "BF": "BFA",
    "BG": "BGR",
    "BA": "BIH",
    "BB": "BRB",
    "WF": "WLF",
    "BL": "BLM",
    "BM": "BMU",
    "BN": "BRN",
    "BO": "BOL",
    "BH": "BHR",
    "BI": "BDI",
    "BJ": "BEN",
    "BT": "BTN",
    "JM": "JAM",
    "BV": "BVT",
    "BW": "BWA",
    "WS": "WSM",
    "BQ": "BES",
    "BR": "BRA",
    "BS": "BHS",
    "JE": "JEY",
    "BY": "BLR",
    "BZ": "BLZ",
    "RU": "RUS",
    "RW": "RWA",
    "RS": "SRB",
    "TL": "TLS",
    "RE": "REU",
    "TM": "TKM",
    "TJ": "TJK",
    "RO": "ROU",
    "TK": "TKL",
    "GW": "GNB",
    "GU": "GUM",
    "GT": "GTM",
    "GS": "SGS",
    "GR": "GRC",
    "GQ": "GNQ",
    "GP": "GLP",
    "JP": "JPN",
    "GY": "GUY",
    "GG": "GGY",
    "GF": "GUF",
    "GE": "GEO",
    "GD": "GRD",
    "GB": "GBR",
    "GA": "GAB",
    "SV": "SLV",
    "GN": "GIN",
    "GM": "GMB",
    "GL": "GRL",
    "GI": "GIB",
    "GH": "GHA",
    "OM": "OMN",
    "TN": "TUN",
    "JO": "JOR",
    "HR": "HRV",
    "HT": "HTI",
    "HU": "HUN",
    "HK": "HKG",
    "HN": "HND",
    "HM": "HMD",
    "VE": "VEN",
    "PR": "PRI",
    "PS": "PSE",
    "PW": "PLW",
    "PT": "PRT",
    "SJ": "SJM",
    "PY": "PRY",
    "IQ": "IRQ",
    "PA": "PAN",
    "PF": "PYF",
    "PG": "PNG",
    "PE": "PER",
    "PK": "PAK",
    "PH": "PHL",
    "PN": "PCN",
    "PL": "POL",
    "PM": "SPM",
    "ZM": "ZMB",
    "EH": "ESH",
    "EE": "EST",
    "EG": "EGY",
    "ZA": "ZAF",
    "EC": "ECU",
    "IT": "ITA",
    "VN": "VNM",
    "SB": "SLB",
    "ET": "ETH",
    "SO": "SOM",
    "ZW": "ZWE",
    "SA": "SAU",
    "ES": "ESP",
    "ER": "ERI",
    "ME": "MNE",
    "MD": "MDA",
    "MG": "MDG",
    "MF": "MAF",
    "MA": "MAR",
    "MC": "MCO",
    "UZ": "UZB",
    "MM": "MMR",
    "ML": "MLI",
    "MO": "MAC",
    "MN": "MNG",
    "MH": "MHL",
    "MK": "MKD",
    "MU": "MUS",
    "MT": "MLT",
    "MW": "MWI",
    "MV": "MDV",
    "MQ": "MTQ",
    "MP": "MNP",
    "MS": "MSR",
    "MR": "MRT",
    "IM": "IMN",
    "UG": "UGA",
    "TZ": "TZA",
    "MY": "MYS",
    "MX": "MEX",
    "IL": "ISR",
    "FR": "FRA",
    "IO": "IOT",
    "SH": "SHN",
    "FI": "FIN",
    "FJ": "FJI",
    "FK": "FLK",
    "FM": "FSM",
    "FO": "FRO",
    "NI": "NIC",
    "NL": "NLD",
    "NO": "NOR",
    "NA": "NAM",
    "VU": "VUT",
    "NC": "NCL",
    "NE": "NER",
    "NF": "NFK",
    "NG": "NGA",
    "NZ": "NZL",
    "NP": "NPL",
    "NR": "NRU",
    "NU": "NIU",
    "CK": "COK",
    "XK": "XKX",
    "CI": "CIV",
    "CH": "CHE",
    "CO": "COL",
    "CN": "CHN",
    "CM": "CMR",
    "CL": "CHL",
    "CC": "CCK",
    "CA": "CAN",
    "CG": "COG",
    "CF": "CAF",
    "CD": "COD",
    "CZ": "CZE",
    "CY": "CYP",
    "CX": "CXR",
    "CR": "CRI",
    "CW": "CUW",
    "CV": "CPV",
    "CU": "CUB",
    "SZ": "SWZ",
    "SY": "SYR",
    "SX": "SXM",
    "KG": "KGZ",
    "KE": "KEN",
    "SS": "SSD",
    "SR": "SUR",
    "KI": "KIR",
    "KH": "KHM",
    "KN": "KNA",
    "KM": "COM",
    "ST": "STP",
    "SK": "SVK",
    "KR": "KOR",
    "SI": "SVN",
    "KP": "PRK",
    "KW": "KWT",
    "SN": "SEN",
    "SM": "SMR",
    "SL": "SLE",
    "SC": "SYC",
    "KZ": "KAZ",
    "KY": "CYM",
    "SG": "SGP",
    "SE": "SWE",
    "SD": "SDN",
    "DO": "DOM",
    "DM": "DMA",
    "DJ": "DJI",
    "DK": "DNK",
    "VG": "VGB",
    "DE": "DEU",
    "YE": "YEM",
    "DZ": "DZA",
    "US": "USA",
    "UY": "URY",
    "YT": "MYT",
    "UM": "UMI",
    "LB": "LBN",
    "LC": "LCA",
    "LA": "LAO",
    "TV": "TUV",
    "TW": "TWN",
    "TT": "TTO",
    "TR": "TUR",
    "LK": "LKA",
    "LI": "LIE",
    "LV": "LVA",
    "TO": "TON",
    "LT": "LTU",
    "LU": "LUX",
    "LR": "LBR",
    "LS": "LSO",
    "TH": "THA",
    "TF": "ATF",
    "TG": "TGO",
    "TD": "TCD",
    "TC": "TCA",
    "LY": "LBY",
    "VA": "VAT",
    "VC": "VCT",
    "AE": "ARE",
    "AD": "AND",
    "AG": "ATG",
    "AF": "AFG",
    "AI": "AIA",
    "VI": "VIR",
    "IS": "ISL",
    "IR": "IRN",
    "AM": "ARM",
    "AL": "ALB",
    "AO": "AGO",
    "AQ": "ATA",
    "AS": "ASM",
    "AR": "ARG",
    "AU": "AUS",
    "AT": "AUT",
    "AW": "ABW",
    "IN": "IND",
    "AX": "ALA",
    "AZ": "AZE",
    "IE": "IRL",
    "ID": "IDN",
    "UA": "UKR",
    "QA": "QAT",
    "MZ": "MOZ",
}
GCS = ["EPGS:4326", "EPGS:3035", "EPGS:3857", "EPGS:4258"]
status_list = [
    "Rejected",
    "Queued",
    "In_progress",
    "Finished_ok",
    "Finished_nok",
    "Cancelled",
]
dataset_formats = [
    "Shapefile",
    "GDB",
    "GPKG",
    "Geojson",
    "Geotiff",
    "Netcdf",
    "GML",
    "WFS",
]
table = {
    "Shapefile": {
        "Shapefile": False,
        "GDB": True,
        "GPKG": True,
        "Geojson": True,
        "Geotiff": False,
        "Netcdf": False,
        "GML": True,
        "WFS": False,
    },
    "GDB": {
        "Shapefile": True,
        "GDB": False,
        "GPKG": True,
        "Geojson": True,
        "Geotiff": False,
        "Netcdf": False,
        "GML": True,
        "WFS": False,
    },
    "GPKG": {
        "Shapefile": True,
        "GDB": True,
        "GPKG": False,
        "Geojson": True,
        "Geotiff": False,
        "Netcdf": False,
        "GML": True,
        "WFS": False,
    },
    "Geojson": {
        "Shapefile": True,
        "GDB": True,
        "GPKG": True,
        "Geojson": False,
        "Geotiff": False,
        "Netcdf": False,
        "GML": True,
        "WFS": False,
    },
    "Geotiff": {
        "Shapefile": False,
        "GDB": False,
        "GPKG": False,
        "Geojson": False,
        "Geotiff": False,
        "Netcdf": False,
        "GML": False,
        "WFS": False,
    },
    "Netcdf": {
        "Shapefile": False,
        "GDB": False,
        "GPKG": False,
        "Geojson": False,
        "Geotiff": True,
        "Netcdf": False,
        "GML": False,
        "WFS": False,
    },
    "WFS": {
        "Shapefile": True,
        "GDB": True,
        "GPKG": True,
        "Geojson": True,
        "Geotiff": False,
        "Netcdf": False,
        "GML": True,
        "WFS": False,
    },
}


class datarequest_status_patch(Service):
    """ Nuts & BBox not at the same time
    """
    def reply(self):
        """ JSON response """
        body = json_body(self.request)
        task_id = str(body.get("TaskID"))
        status = body.get("Status")
        user_id = body.get("UserID")
        download_url = body.get("DownloadURL")
        filesize = body.get("FileSize")

        response_json = {}

        utility = getUtility(IDownloadToolUtility)

        if not task_id:
            self.request.response.setStatus(400)
            return {"status": "error", "msg":"Error, TaskID is not defined"}

        if not status:
            self.request.response.setStatus(400)
            return {"status": "error", "msg":"Error, Status is not defined"}

        if status not in status_list:
            self.request.response.setStatus(400)
            return {"status": "error", "msg":"Error, defined Status is not in the list"}
        response_json = {"TaskID": task_id, "Status": status}

        if filesize:
            response_json.update({"FileSize": filesize})
        
        if download_url:
            response_json.update({"DownloadURL": download_url})

        log.info(response_json)
        response_json = utility.datarequest_status_patch(
            response_json, task_id
        )

        log.info(response_json)


        if "Error, task_id not registered" in response_json:
            self.request.response.setStatus(404)
            return {"status": "error", "msg":response_json}

        if (
            "Error, NUTSID and BoundingBox can't be defined in the same task"
            in response_json
        ):
            self.request.response.setStatus(400)
            return{"status": "error", "msg":response_json}

        if "Error" in response_json:
            self.request.response.setStatus(400)
            return {"status": "error", "msg":response_json}
            
        self.request.response.setStatus(201)

        return response_json
