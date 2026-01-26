from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class ServiceOwner(BaseModel):
    id: str
    name: str
    email: Optional[str] = None
    type: str

class ServiceDetail(BaseModel):
    id: str
    name: str
    type: str # static_site, web_service, private_service, background_worker, cron_job
    status: str
    updatedAt: datetime
    createdAt: datetime
    serviceDetails: Optional[Dict[str, Any]] = None
    repo: Optional[str] = None
    ownerId: Optional[str] = None

class RenderService(BaseModel):
    service: ServiceDetail

class ServiceList(BaseModel):
    services: List[RenderService]

class UnifiedService(BaseModel):
    id: str
    name: str
    type: str
    status: str
    url: Optional[str] = None
    repo: Optional[str] = None
    updated_at: datetime
    owner_name: Optional[str] = None
