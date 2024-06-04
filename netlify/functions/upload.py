import json
from app import upload_file

def handler(event, context):
    return upload_file()
