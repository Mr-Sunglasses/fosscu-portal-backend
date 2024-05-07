import httpx
from .constant import AIRTABLE_API_TOKEN
import json


async def _get_airtable_data():
    async with httpx.AsyncClient() as client:
        url = "https://api.airtable.com/v0/app56OIvmSDDANlXb/Table%201"
        headers = {'Authorization': f'Bearer {AIRTABLE_API_TOKEN}'}
        request = await client.get(url, headers=headers)
    data = request.json()
    data = [record['fields'] for record in data['records']]
    data_str = json.dumps(data)
    return data_str
