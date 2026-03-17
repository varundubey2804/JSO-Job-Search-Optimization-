import os
import json
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Check for both SDKs
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

try:
    import google.generativeai as genai
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False

class LLMService:
    def __init__(self):
        # Groq Config
        self.groq_key = os.getenv("GROQ_API_KEY", "")
        self.groq_model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        
        # Google Config
        self.google_key = os.getenv("GOOGLE_AI_API_KEY", "")
        self.google_model = "gemini-1.5-flash"
        
        self.groq_client = None
        self.google_client = None

        if GROQ_AVAILABLE and self.groq_key:
            try:
                self.groq_client = Groq(api_key=self.groq_key)
                logger.info("Groq client initialized")
            except Exception as e:
                logger.error(f"Groq init error: {e}")

        if GOOGLE_AVAILABLE and self.google_key:
            try:
                genai.configure(api_key=self.google_key)
                self.google_client = genai.GenerativeModel(self.google_model)
                logger.info("Google AI client initialized")
            except Exception as e:
                logger.error(f"Google AI init error: {e}")

    def generate_completion(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None, 
        json_mode: bool = False
    ) -> str:
        """
        Send prompt to LLM, attempting Groq first, then Google AI, then Mock.
        """
        # 1. Primary Attempt: Groq
        if self.groq_client:
            try:
                return self._call_groq(prompt, system_prompt, json_mode)
            except Exception as e:
                logger.warning(f"Groq failed: {e}. Attempting Google AI fallback...")

        # 2. Secondary Attempt: Google AI
        if self.google_client:
            try:
                return self._call_google(prompt, system_prompt, json_mode)
            except Exception as e:
                logger.error(f"Google AI failed: {e}. Falling back to mock.")

        # 3. Final Fallback: Mock
        return self._mock_completion(prompt, json_mode)

    def _call_groq(self, prompt, system_prompt, json_mode):
        messages = []
        
        # CRITICAL FIX: Groq/Llama requires explicitly mentioning JSON in the prompt
        if json_mode and system_prompt:
            system_prompt += " You must output ONLY valid JSON."
            
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
            
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.groq_model,
            "messages": messages,
            "temperature": 0.2,
        }
        
        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        response = self.groq_client.chat.completions.create(**payload)
        return response.choices[0].message.content

    def _call_google(self, prompt, system_prompt, json_mode):
        combined_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        
        generation_config = {"temperature": 0.2}
        if json_mode:
            generation_config["response_mime_type"] = "application/json"

        response = self.google_client.generate_content(
            combined_prompt,
            generation_config=generation_config
        )
        return response.text

    def _mock_completion(self, prompt: str, json_mode: bool) -> str:
        logger.info("Using Mock LLM Response")

        if "extract skills" in prompt.lower():
            res = {
                "skills": ["Python", "TensorFlow", "Machine Learning", "Data Analysis"]
            }
        elif "boolean" in prompt.lower() and "x-ray" in prompt.lower():
            res = {
                "boolean_query": '("Machine Learning Engineer" OR "AI Engineer") AND (Python OR TensorFlow)',
                "xray_query": 'site:linkedin.com/in ("Machine Learning Engineer") ("Python" OR "TensorFlow")'
            }
        else:
            res = {"result": "Mock LLM Response"}

        return json.dumps(res) if json_mode else str(res)

llm_service = LLMService()