from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from models.schemas import (
    GenerateQueryRequest, GenerateQueryResponse, 
    ExtractedSkillsResponse, QueryHistoryResponse, 
    AnalyticsResponse
)
from api.auth import verify_token, require_role
from agent.job_agent import job_agent
import logging
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter()

# Mock Database for Prototype (Replace with Supabase)
mock_query_history = []

@router.post("/generate-query", response_model=GenerateQueryResponse)
async def generate_query(request: GenerateQueryRequest, user: dict = Depends(verify_token)):
    logger.info(f"User {user['user_id']} requested query generation for {request.role}")
    
    try:
        result = job_agent.process_job_search_request(
            role=request.role,
            skills=request.skills,
            experience=request.experience,
            location=request.location,
            platform=request.platform
        )
        
        # Save to mock history
        history_item = {
            "id": str(uuid.uuid4()),
            "user_id": user["user_id"],
            "role": request.role,
            "platform": request.platform,
            "boolean_query": result["boolean_query"],
            "xray_query": result["xray_query"],
            "created_at": datetime.now().isoformat()
        }
        mock_query_history.append(history_item)
        
        return GenerateQueryResponse(**result)
    except Exception as e:
        logger.error(f"Error generating query: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate query")


@router.post("/extract-skills", response_model=ExtractedSkillsResponse)
async def extract_skills(file: UploadFile = File(...), user: dict = Depends(require_role(["HR Consultant", "Admin"]))):
    logger.info(f"User {user['user_id']} uploading resume for skill extraction")
    try:
        content = await file.read()
        try:
            text_content = content.decode('utf-8') # Simplification for prototype: expects text/plain.
        except UnicodeDecodeError:
            text_content = content.decode('utf-8', errors='ignore') # Ignore decode errors for binary files in prototype
            
        skills = job_agent.extract_skills_from_resume(text_content)
        return ExtractedSkillsResponse(skills=skills)
    except Exception as e:
        logger.error(f"Error extracting skills: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to extract skills: {str(e)}")


@router.get("/query-history", response_model=QueryHistoryResponse)
async def query_history(user: dict = Depends(verify_token)):
    logger.info(f"User {user['user_id']} requesting query history")
    # Filter for user (unless Admin)
    if user["role"] == "Admin":
        history = mock_query_history
    else:
        history = [h for h in mock_query_history if h["user_id"] == user["user_id"]]
    
    return QueryHistoryResponse(history=history)


@router.get("/analytics", response_model=AnalyticsResponse)
async def get_analytics(user: dict = Depends(require_role(["Admin", "Licensing Manager"]))):
    logger.info(f"User {user['user_id']} requesting analytics")
    
    # Mock Analytics Data
    return AnalyticsResponse(
        queries_per_day={"2023-10-24": 150, "2023-10-25": 200, "2023-10-26": 320},
        active_users=1050,
        top_roles={"Machine Learning Engineer": 500, "Data Scientist": 450, "Software Engineer": 400}
    )
