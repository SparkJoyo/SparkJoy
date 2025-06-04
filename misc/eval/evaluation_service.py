from typing import List, Dict, Any
from openai import OpenAI
from app.config import OPENAI_API_KEY
import json
import logging
from app.models.story import StoryRequest, StoryResponse

class StoryEvaluator:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.evaluation_criteria = {
            "creativity": "How creative and unique is the story?",
            "engagement": "How engaging and captivating is the story for children?",
            "coherence": "How well-structured and coherent is the story?",
            "age_appropriateness": "How well does the story match the target age group (3-6 years)?",
            "instruction_following": "How well does the story follow the given instructions and incorporate the required elements?"
        }

    def generate_story_with_provider(self, provider: str, prompt: str) -> str:
        """Generate a story using the specified LLM provider."""
        try:
            if provider == "openai":
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a friendly bedtime storyteller for young children."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=600,
                    temperature=0.85
                )
                return response.choices[0].message.content.strip()
            # Add more providers here as needed
            else:
                raise ValueError(f"Unsupported provider: {provider}")
        except Exception as e:
            logging.error(f"Error generating story with {provider}: {str(e)}")
            return None

    def evaluate_story(self, story: str, original_request: StoryRequest) -> Dict[str, Any]:
        """Use LLM-as-a-judge to evaluate the story."""
        evaluation_prompt = f"""
        Please evaluate the following children's story based on these criteria:
        {json.dumps(self.evaluation_criteria, indent=2)}

        Original request details:
        - Length: {original_request.length}
        - Instructions: {original_request.instructions}
        - Image elements: {original_request.image_keys}

        Story to evaluate:
        {story}

        Please provide:
        1. A score from 1-10 for each criterion
        2. A brief explanation for each score
        3. Overall strengths and weaknesses
        4. Suggestions for improvement

        Format your response as a JSON object with the following structure:
        {{
            "scores": {{
                "creativity": {{"score": 8, "explanation": "..."}},
                "engagement": {{"score": 7, "explanation": "..."}},
                "coherence": {{"score": 9, "explanation": "..."}},
                "age_appropriateness": {{"score": 8, "explanation": "..."}},
                "instruction_following": {{"score": 7, "explanation": "..."}}
            }},
            "overall_analysis": {{
                "strengths": ["..."],
                "weaknesses": ["..."],
                "suggestions": ["..."]
            }}
        }}
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",  # Using GPT-4 for more reliable evaluation
                messages=[
                    {"role": "system", "content": "You are an expert evaluator of children's stories."},
                    {"role": "user", "content": evaluation_prompt}
                ],
                temperature=0.3  # Lower temperature for more consistent evaluations
            )
            
            evaluation = json.loads(response.choices[0].message.content.strip())
            return evaluation
        except Exception as e:
            logging.error(f"Error evaluating story: {str(e)}")
            return None

    def compare_providers(self, providers: List[str], story_request: StoryRequest) -> Dict[str, Any]:
        """Compare story generation across different providers."""
        results = {}
        
        # Generate stories from each provider
        for provider in providers:
            story = self.generate_story_with_provider(provider, story_request)
            if story:
                evaluation = self.evaluate_story(story, story_request)
                results[provider] = {
                    "story": story,
                    "evaluation": evaluation
                }
        
        return results

    def generate_comparison_report(self, results: Dict[str, Any]) -> str:
        """Generate a human-readable comparison report."""
        report = ["# Story Generation Provider Comparison Report\n"]
        
        for provider, data in results.items():
            report.append(f"## {provider.upper()}\n")
            report.append("### Story")
            report.append(f"```\n{data['story']}\n```\n")
            
            if data['evaluation']:
                report.append("### Evaluation")
                scores = data['evaluation']['scores']
                report.append("#### Scores")
                for criterion, score_data in scores.items():
                    report.append(f"- {criterion}: {score_data['score']}/10")
                    report.append(f"  - {score_data['explanation']}")
                
                analysis = data['evaluation']['overall_analysis']
                report.append("\n#### Overall Analysis")
                report.append("Strengths:")
                for strength in analysis['strengths']:
                    report.append(f"- {strength}")
                report.append("\nWeaknesses:")
                for weakness in analysis['weaknesses']:
                    report.append(f"- {weakness}")
                report.append("\nSuggestions:")
                for suggestion in analysis['suggestions']:
                    report.append(f"- {suggestion}")
            
            report.append("\n---\n")
        
        return "\n".join(report) 