from pydantic import BaseModel, Field
from typing import List, Optional

class GenerateQueryRequest(BaseModel):
    role: str
    skills: List[str]
    experience: str
    location: str
    platform: str

class GenerateQueryResponse(BaseModel):
    boolean_query: str
    xray_query: str
    search_links: List[str]

class ExtractedSkillsResponse(BaseModel):
    skills: List[str]

class QueryHistoryItem(BaseModel):
    id: str
    role: str
    platform: str
    boolean_query: str
    xray_query: str
    created_at: str

class QueryHistoryResponse(BaseModel):
    history: List[QueryHistoryItem]

class AnalyticsResponse(BaseModel):
    queries_per_day: dict
    active_users: int
    top_roles: dict
