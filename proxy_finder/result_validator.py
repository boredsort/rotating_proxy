from datetime import datetime
import json

from schema import Schema, Optional

proxy_info_schema = Schema({
    "meta": {
        "source_url": str,
        "extraction_date": datetime
    },
    "data": {
        "ip": str,
        "port": int,
        "country": str,
        "protocol": str,
        Optional("region"): str,
        Optional("city"): str,
        Optional("anonymity"): str,
        Optional("uptime"): str
    }
})

def validate(proxy_info_json:json)->bool:
    return proxy_info_schema.validate(proxy_info_json)

