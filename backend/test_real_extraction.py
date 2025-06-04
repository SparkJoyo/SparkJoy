#!/usr/bin/env python3
"""
Test real LLM-based requirements extraction
"""

import sys
import os
import json
import logging
from dotenv import load_dotenv

# Configure logging to see all the debug info
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

# Load environment variables
load_dotenv()

# Add app to path
sys.path.append('app')

def test_real_extraction():
    """Test LLM extraction with various prompts"""
    
    # Check API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment!")
        return
    
    print(f"✅ Found API key: {api_key[:10]}...")
    
    # Import service
    from app.services.requirements_service import requirements_service
    
    # Test prompts
    test_prompts = [
        "want to have a story for ella who is 4 years old; it's about sharing is caring",

        # "Write a 5-minute bedtime story for Emma, age 4, about a brave princess who learns sharing. No scary parts.",
     
        # "Tell my twin boys Alex and Ben (they're 6 years old) a quick story about dinosaurs and friendship. Avoid violence.",
        
        # "I need a story for my 3-year-old daughter about a unicorn. Teach kindness and helping others."
    ]
    
    print("\n🚀 Testing LLM Extraction")
    print("=" * 50)
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n📝 Test {i}:")
        print(f"Prompt: {prompt}")
        print("\n🔄 Calling OpenAI API...")
        
        try:
            result = requirements_service.extract_requirements(prompt, user_id=f"test_user_{i}")
            
            print("✅ Extraction successful!")
            print("\n📊 Results:")
            print(json.dumps(result, indent=2))
            
            if result.get('extraction_error'):
                print(f"⚠️  Warning: {result['extraction_error']}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        print("\n" + "-" * 50)

if __name__ == "__main__":
    test_real_extraction() 