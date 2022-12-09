from datetime import datetime
import json

from schema import Schema, Optional

result_schema = Schema({
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

def validate(result_json:json)->bool:
    return result_schema.validate(result_json)

