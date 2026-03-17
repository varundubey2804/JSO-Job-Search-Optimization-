import json
from services.llm_service import llm_service
import urllib.parse
import logging

logger = logging.getLogger(__name__)

class PlatformAdapter:
    """
    Agent responsible for translating general boolean/x-ray queries 
    into platform-specific syntax and generating search URLs.
    """
    def __init__(self):
        self.platform_urls = {
            "LinkedIn": {
                "base_url": "https://www.linkedin.com/search/results/people/?keywords=",
                "site_search": "site:linkedin.com/in"
            },
            "Indeed": {
                "base_url": "https://www.indeed.com/resumes?q=",
                "site_search": "site:indeed.com/resume"
            },
            "Naukri": {
                "base_url": "https://www.naukri.com/resumes?q=",
                "site_search": "site:naukri.com/resume"
            },
            "Glassdoor": {
                "base_url": "https://www.glassdoor.com/resumes?q=",
                "site_search": "site:glassdoor.com/resume"
            },
            "Reed": {
                "base_url": "https://www.reed.co.uk/cvs?q=",
                "site_search": "site:reed.co.uk/cv"
            },
            "TotalJobs": {
                "base_url": "https://www.totaljobs.com/cvs?q=",
                "site_search": "site:totaljobs.com/cv"
            }
        }
        
    def adapt_queries(self, base_queries: dict, platform: str, location: str) -> dict:
        """
        Takes the base queries and modifies them for the specific platform.
        """
        p_info = self.platform_urls.get(platform, self.platform_urls["LinkedIn"])
        
        boolean_query = base_queries.get("boolean_query", "")
        xray_base = base_queries.get("xray_base", "")
        
        # Add platform specific syntax if needed. For prototype, we just append to the base.
        # Construct the X-Ray query
        xray_query = f'{p_info["site_search"]} {xray_base} "{location}"'
        
        # Construct search links
        encoded_boolean = urllib.parse.quote(boolean_query)
        encoded_xray = urllib.parse.quote(xray_query)
        
        search_links = [
            f"{p_info['base_url']}{encoded_boolean}",
            f"https://www.google.com/search?q={encoded_xray}"
        ]
        
        return {
            "boolean_query": boolean_query,
            "xray_query": xray_query,
            "search_links": search_links
        }

platform_adapter = PlatformAdapter()
