from datetime import datetime
import json

from schema import Schema, Optional

# proxy_data_schema = Schema({
#     "meta": {
#         "source_url": str,
#         "extraction_date": datetime
#     },
#     "data": {
#         "ip": str,
#         "port": int,
#         "country": str,
#         "protocol": str,
#         Optional("region"): str,
#         Optional("city"): str,
#         Optional("anonymity"): str,
#         Optional("uptime"): str
#     }
# })

proxy_data_schema = Schema({
    "ip": str,
    "port": int,
    "country": str,
    "protocols": list,
    Optional("region"): str,
    Optional("city"): str,
    Optional("anonymity"): str,
    Optional("uptime"): str
})


def validate(proxy_data_json:json)->bool:
    return proxy_data_schema.validate(proxy_data_json)

