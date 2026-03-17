import json
from services.llm_service import llm_service
import logging

logger = logging.getLogger(__name__)

class QueryGenerator:
    """
    Agent responsible for generating base boolean queries
    based on the job requirements.
    """
    def __init__(self):
        self.system_prompt = """
        You are an expert Talent Sourcing Query Generator.
        Your task is to take job requirements and create highly optimized Boolean search strings.
        Output ONLY valid JSON matching this schema:
        {
          "boolean_query": "(JobTitle OR Synonym) AND (Skill1 OR Synonym) AND ...",
          "xray_base": "site:example.com/in (JobTitle) (Skills)"
        }
        """

    def generate_base_queries(self, role: str, skills: list[str], experience: str, location: str) -> dict:
        prompt = f"""
        Generate sourcing queries for the following requirements:
        Role: {role}
        Skills: {', '.join(skills)}
        Experience: {experience}
        Location: {location}
        """
        response = llm_service.generate_completion(
            prompt=prompt,
            system_prompt=self.system_prompt,
            json_mode=True
        )
        
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode QueryGenerator JSON: {e}")
            return {
                "boolean_query": f'("{role}") AND ({ " OR ".join(skills) })',
                "xray_base": f'("{role}") ({ " OR ".join(skills) })'
            }

query_generator = QueryGenerator()
