import httpx
from .constant import AIRTABLE_API_TOKEN
import json
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def _get_airtable_data():
    """
    Fetch data from Airtable API with improved error handling
    """
    try:
        # Get token from environment variable directly as a fallback
        token = AIRTABLE_API_TOKEN or os.getenv("AIRTABLE_API_TOKEN")
        
        # Debug token (display only first few characters for security)
        if token:
            logger.info(f"Using Airtable token: {token[:4]}...")
        else:
            logger.error("AIRTABLE_API_TOKEN is not set or empty")
            return json.dumps([{"Name": "API Token Error", "Discord Username": "N/A", "XP": 0}])
            
        async with httpx.AsyncClient() as client:
            url = "https://api.airtable.com/v0/app56OIvmSDDANlXb/Table%201"
            headers = {'Authorization': f'Bearer {token}'}
            
            logger.info(f"Making request to Airtable API: {url}")
            response = await client.get(url, headers=headers, timeout=30.0)
            
            # Log the status code
            logger.info(f"Airtable API response status: {response.status_code}")
            
            # Check for successful response
            response.raise_for_status()
            
            # Parse the JSON response
            text_response = response.text
            logger.info(f"Response preview: {text_response[:100]}...")  # Log first 100 chars
            
            data = response.json()
            
            # Log response structure for debugging
            logger.info(f"Response keys: {list(data.keys() if isinstance(data, dict) else ['NOT_A_DICT'])}")
            
            # Check if 'records' key exists
            if not isinstance(data, dict) or 'records' not in data:
                logger.error(f"No 'records' key in Airtable response. Response preview: {str(data)[:200]}")
                if isinstance(data, dict) and 'error' in data:
                    logger.error(f"Airtable error: {data['error']}")
                
                # Return a dummy entry to avoid breaking the UI
                return json.dumps([{"Name": "API Response Error", "Discord Username": "Check logs", "XP": 0}])
            
            # Extract fields from each record
            records = [record['fields'] for record in data['records']]
            logger.info(f"Successfully extracted {len(records)} records from Airtable")
            
            # Ensure all records have the required fields
            processed_records = []
            for record in records:
                processed_record = {
                    "Name": record.get("Name", "Unknown"),
                    "Discord Username": record.get("Discord Username", "N/A"),
                    "XP": float(record.get("XP", 0))
                }
                processed_records.append(processed_record)
            
            data_str = json.dumps(processed_records)
            logger.info(f"Returning JSON data with {len(processed_records)} records")
            return data_str
            
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error occurred: {e}")
        logger.error(f"Response content: {e.response.text[:500]}...")
        error_message = f"Status code: {e.response.status_code}"
        return json.dumps([{"Name": "HTTP Error", "Discord Username": error_message, "XP": 0}])
        
    except httpx.RequestError as e:
        logger.error(f"Request error occurred: {e}")
        return json.dumps([{"Name": "Connection Error", "Discord Username": str(e), "XP": 0}])
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        return json.dumps([{"Name": "JSON Parse Error", "Discord Username": "Invalid response format", "XP": 0}])
        
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        logger.exception("Full exception details:")
        return json.dumps([{"Name": "Error", "Discord Username": str(e), "XP": 0}])