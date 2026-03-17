import os
import json
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Check Groq availability
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False


class LLMService:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY", "")
        self.base_url = os.getenv("GROQ_BASE_URL", "")
        self.model = os.getenv("GROQ_MODEL", "llama3-70b-8192")
        self.use_mock = not bool(self.api_key) or not GROQ_AVAILABLE

        if not self.use_mock:
            try:
                if self.base_url:
                    self.client = Groq(api_key=self.api_key, base_url=self.base_url)
                else:
                    self.client = Groq(api_key=self.api_key)
                logger.info("Groq client initialized successfully")
            except Exception as e:
                logger.warning(f"Groq init failed: {e}. Using mock responses.")
                self.use_mock = True

    def generate_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        json_mode: bool = False
    ) -> str:
        """
        Send prompt to LLM and return response.
        """

        if self.use_mock:
            return self._mock_completion(prompt, json_mode)

        try:
            messages = []

            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })

            messages.append({
                "role": "user",
                "content": prompt
            })

            request_payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.2
            }

            if json_mode:
                request_payload["response_format"] = {"type": "json_object"}

            response = self.client.chat.completions.create(**request_payload)

            result = response.choices[0].message.content

            if json_mode:
                try:
                    json.loads(result)
                except Exception:
                    logger.warning("LLM returned invalid JSON, fixing.")
                    result = json.dumps({"result": result})

            return result

        except Exception as e:
            logger.error(f"LLM API error: {e}")
            return self._mock_completion(prompt, json_mode)

    def _mock_completion(self, prompt: str, json_mode: bool) -> str:
        """
        Mock LLM responses for offline testing
        """

        logger.info("Using Mock LLM Response")

        if "extract skills" in prompt.lower():
            res = {
                "skills": [
                    "Python",
                    "TensorFlow",
                    "Machine Learning",
                    "Data Analysis"
                ]
            }

        elif "boolean" in prompt.lower() and "x-ray" in prompt.lower():
            res = {
                "boolean_query":
                '("Machine Learning Engineer" OR "AI Engineer") AND (Python OR TensorFlow)',

                "xray_query":
                'site:linkedin.com/in ("Machine Learning Engineer") ("Python" OR "TensorFlow")'
            }

        else:
            res = {"result": "Mock LLM Response"}

        return json.dumps(res) if json_mode else str(res)


# Singleton
llm_service = LLMService()