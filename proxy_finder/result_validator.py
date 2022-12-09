from datetime import datetime
from typing import Optional
import json

from schema import Schema

result_schema = Schema({
    "meta": {
        "source_url": str,
        "date": datetime
    },
    "data": {
        "ip": str,
        "port": int,
        "country": str,
        "protocol": str,
        "region": Optional(str),
        "city": Optional(str),
        "anonymity": Optional(str),
        "uptime": Optional(str)
    }
})

def validate(result_json:json)->bool:
    return result_schema.validate(result_json)

