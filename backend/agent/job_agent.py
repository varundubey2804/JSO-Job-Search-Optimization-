from agent.skill_extractor import skill_extractor
from agent.query_generator import query_generator
from agent.platform_adapter import platform_adapter
import logging

logger = logging.getLogger(__name__)

class JobAgentOrchestrator:
    """
    Main entry point for the Job Search Optimization Agentic Workflow.
    Coordinates between SkillExtractor, QueryGenerator, and PlatformAdapter.
    """
    def __init__(self):
        self.skill_extractor = skill_extractor
        self.query_generator = query_generator
        self.platform_adapter = platform_adapter

    def process_job_search_request(self, role: str, skills: list[str], experience: str, location: str, platform: str) -> dict:
        """
        Orchestrates the entire query generation workflow.
        """
        logger.info(f"Starting job search agent for role: {role} on platform: {platform}")
        
        # 1. (Optional) Re-extract/enhance skills if necessary. 
        # For now, we assume skills are provided directly by user input in the dashboard.
        enhanced_skills = skills # In a full system, you might ask the LLM for synonyms.
        
        # 2. Generate Base Queries
        base_queries = self.query_generator.generate_base_queries(
            role=role,
            skills=enhanced_skills,
            experience=experience,
            location=location
        )
        
        # 3. Adapt to Platform
        final_queries = self.platform_adapter.adapt_queries(
            base_queries=base_queries,
            platform=platform,
            location=location
        )
        
        return final_queries

    def extract_skills_from_resume(self, text: str) -> list[str]:
        """
        Uses the skill extractor agent to parse resume text.
        """
        logger.info("Extracting skills from resume")
        return self.skill_extractor.extract_from_text(text)

job_agent = JobAgentOrchestrator()
