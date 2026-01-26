import httpx
import os
from typing import List, Dict, Any
from .models import UnifiedService
from dotenv import load_dotenv

load_dotenv()

RENDER_API_URL = "https://api.render.com/v1"
API_KEY = os.getenv("RENDER_API_KEY")

async def get_services() -> List[UnifiedService]:
    if not API_KEY:
        return []

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json"
    }

    async with httpx.AsyncClient() as client:
        # Fetch Services
        response = await client.get(f"{RENDER_API_URL}/services?limit=100", headers=headers)
        if response.status_code != 200:
            return []
        
        raw_services = response.json()
        unified_services = []
        
        for item in raw_services:
            # Render API returns a list of objects where each object has a 'service' key
            svc = item.get("service", {})
            
            # Extract URL if available
            url = None
            details = svc.get("serviceDetails", {})
            if svc.get("type") == "static_site":
                url = details.get("url")
            elif svc.get("type") == "web_service":
                url = details.get("url")
            
            unified_services.append(UnifiedService(
                id=svc.get("id"),
                name=svc.get("name"),
                type=svc.get("type"),
                status=svc.get("status"),
                url=url,
                repo=svc.get("repo"),
                updated_at=svc.get("updatedAt"),
                owner_name=None # We could fetch owners separately if needed
            ))
            
        return unified_services

async def get_owners() -> List[Dict[str, Any]]:
    if not API_KEY:
        return []
        
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{RENDER_API_URL}/owners", headers=headers)
        if response.status_code == 200:
            return response.json()
        return []
