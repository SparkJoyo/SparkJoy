"""
LLM-based requirements extraction service.
Extracts only: age, length, names, characters, educational behavior, avoid topics.
Everything else goes to additional requirements.
"""

import json
import os
import logging
from typing import Dict, List, Optional
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logger
logger = logging.getLogger(__name__)

class RequirementsService:
    """LLM-based service to extract specific fields from story prompts"""
    
    def __init__(self):
        """Initialize with OpenAI client"""
        logger.info("Initializing RequirementsService")
        try:
            self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            self.extraction_prompt = self._build_extraction_prompt()
            logger.info("RequirementsService initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize RequirementsService: {str(e)}")
            raise
    
    def _build_extraction_prompt(self) -> str:
        """Build the LLM prompt for focused extraction"""
        return """You are an expert at extracting specific information from children's story requests. 

Extract ONLY these specific fields from the parent's prompt:

1. **ages**: List of child ages as integers (e.g., [4, 6])
2. **length**: Story length as string (e.g., "5 minutes", "short", "quick", "long") 
3. **names**: List of child names mentioned (e.g., ["Emma", "Jack"])
4. **characters**: List of story characters/animals (e.g., ["princess", "dragon", "dog"])
5. **educational_behavior**: List of behaviors/values to teach (e.g., ["sharing", "kindness", "friendship"])
6. **avoid_topics**: List of topics to avoid (e.g., ["scary content", "sad themes"])

IMPORTANT: Return ONLY a valid JSON object with these exact field names. If a field has no information, use an empty list [] or null.

Parent's request: {prompt}

Respond with JSON only:"""

    def extract_requirements(self, prompt: str, user_id: Optional[str] = None) -> Dict:
        """
        Extract specific structured fields from prompt using LLM
        
        Returns:
        {
            "ages": [list of integers],
            "length": string or None,
            "names": [list of child names],
            "characters": [list of story characters],
            "educational_behavior": [list of educational elements],
            "avoid_topics": [list of topics to avoid],
            "additional_requirements": [original prompt],
            "extraction_error": error message or None
        }
        """
        user_context = f"user {user_id}" if user_id else "anonymous user"
        logger.info(f"Starting requirements extraction for {user_context}")
        logger.debug(f"Input prompt length: {len(prompt)} characters")
        
        try:
            # Call OpenAI API
            full_prompt = self.extraction_prompt.format(prompt=prompt)
            logger.debug(f"Built extraction prompt for {user_context}")
            
            logger.info(f"Making OpenAI API call for {user_context}")
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts information and returns only valid JSON."},
                    {"role": "user", "content": full_prompt}
                ],
                max_tokens=500,
                temperature=0.1
            )
            
            logger.info(f"Received OpenAI API response for {user_context}")
            logger.debug(f"Response usage: {response.usage}")
            
            # Parse LLM response
            content = response.choices[0].message.content.strip()
            logger.debug(f"Raw LLM response length: {len(content)} characters")
            logger.debug(f"Raw LLM response: {content}")
            
            # Clean up response (remove any markdown formatting)
            original_content = content
            if content.startswith('```json'):
                content = content[7:]
                logger.debug("Removed ```json prefix")
            if content.endswith('```'):
                content = content[:-3]
                logger.debug("Removed ``` suffix")
            content = content.strip()
            
            if content != original_content:
                logger.debug("Cleaned markdown formatting from response")
            
            # Parse JSON
            logger.debug(f"Attempting to parse JSON response for {user_context}")
            extracted_data = json.loads(content)
            logger.info(f"Successfully parsed JSON response for {user_context}")
            logger.debug(f"Extracted fields: {list(extracted_data.keys())}")
            
            # Ensure all required fields exist with correct types
            result = {
                "ages": self._ensure_list_of_ints(extracted_data.get("ages", [])),
                "length": extracted_data.get("length"),
                "names": self._ensure_list_of_strings(extracted_data.get("names", [])),
                "characters": self._ensure_list_of_strings(extracted_data.get("characters", [])),
                "educational_behavior": self._ensure_list_of_strings(extracted_data.get("educational_behavior", [])),
                "avoid_topics": self._ensure_list_of_strings(extracted_data.get("avoid_topics", [])),
                "additional_requirements": [prompt.strip()],  # Always include original prompt
                "extraction_error": None
            }
            
            logger.info(f"Successfully extracted requirements for {user_context}")
            logger.debug(f"Final result summary - ages: {len(result['ages'])}, names: {len(result['names'])}, characters: {len(result['characters'])}")
            
            return result
            
        except json.JSONDecodeError as e:
            error_msg = f"JSON parsing error: {str(e)}"
            logger.warning(f"JSON parsing failed for {user_context}: {error_msg}")
            logger.debug(f"Failed to parse content: {content[:200]}...")
            return self._fallback_result(prompt, error_msg)
            
        except Exception as e:
            error_msg = f"Extraction error: {str(e)}"
            logger.error(f"Requirements extraction failed for {user_context}: {error_msg}")
            logger.debug(f"Exception details: {type(e).__name__}: {str(e)}")
            return self._fallback_result(prompt, error_msg)
    
    def _ensure_list_of_ints(self, value) -> List[int]:
        """Ensure value is a list of integers"""
        if not isinstance(value, list):
            logger.debug(f"Converting non-list value to list for ages: {type(value)}")
            return []
        result = []
        for item in value:
            try:
                if isinstance(item, int):
                    result.append(item)
                elif isinstance(item, str) and item.isdigit():
                    result.append(int(item))
                    logger.debug(f"Converted string age to int: {item}")
            except Exception as e:
                logger.debug(f"Skipped invalid age value: {item} ({str(e)})")
                continue
        logger.debug(f"Processed ages: {result}")
        return result
    
    def _ensure_list_of_strings(self, value) -> List[str]:
        """Ensure value is a list of strings"""
        if not isinstance(value, list):
            logger.debug(f"Converting non-list value to list: {type(value)}")
            return []
        result = [str(item) for item in value if item]
        logger.debug(f"Processed string list: {len(result)} items")
        return result
    
    def _fallback_result(self, prompt: str, error: str) -> Dict:
        """Return fallback result when LLM extraction fails"""
        logger.warning(f"Using fallback result due to: {error}")
        return {
            "ages": [],
            "length": None,
            "names": [],
            "characters": [],
            "educational_behavior": [],
            "avoid_topics": [],
            "additional_requirements": [prompt.strip()],
            "extraction_error": error
        }

# Singleton instance
requirements_service = RequirementsService() 