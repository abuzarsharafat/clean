import json
from app import clean_file

def handler(event, context):
    return clean_file()
