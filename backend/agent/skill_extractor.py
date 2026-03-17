import json
from services.llm_service import llm_service
import logging

logger = logging.getLogger(__name__)

class SkillExtractor:
    """
    Agent responsible for analyzing resumes or profile text
    and extracting key skills and experiences.
    """
    def __init__(self):
        self.system_prompt = """
        You are an expert HR Data Extraction Agent. 
        Your task is to analyze resume text and extract technical and soft skills.
        Return ONLY valid JSON matching this schema:
        {
          "skills": ["Skill1", "Skill2"]
        }
        """

    def extract_from_text(self, text: str) -> list[str]:
        prompt = f"Extract all skills from this text:\n\n{text}"
        response = llm_service.generate_completion(
            prompt=prompt,
            system_prompt=self.system_prompt,
            json_mode=True
        )
        
        try:
            data = json.loads(response)
            return data.get("skills", [])
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode SkillExtractor JSON: {e}")
            return []

skill_extractor = SkillExtractor()
