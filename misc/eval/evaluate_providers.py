from app.services.evaluation_service import StoryEvaluator
from app.models.story import StoryRequest
import json
from datetime import datetime
import os

def main():
    # Create evaluation directory if it doesn't exist
    eval_dir = "evaluation_results"
    os.makedirs(eval_dir, exist_ok=True)

    # Initialize the evaluator
    evaluator = StoryEvaluator()

    # Create a sample story request
    story_request = StoryRequest(
        length="Medium",
        instructions="Create a story about a magical garden where plants can talk",
        image_keys=["garden.jpg", "flowers.jpg", "butterfly.jpg"]
    )

    # List of providers to compare
    providers = ["openai"]  # Add more providers as they are implemented

    # Run the comparison
    print("Starting provider comparison...")
    results = evaluator.compare_providers(providers, story_request)

    # Generate the report
    report = evaluator.generate_comparison_report(results)

    # Save the report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(eval_dir, f"comparison_report_{timestamp}.md")
    
    with open(report_path, "w") as f:
        f.write(report)

    print(f"\nEvaluation complete! Report saved to: {report_path}")

    # Also save the raw results as JSON
    json_path = os.path.join(eval_dir, f"raw_results_{timestamp}.json")
    with open(json_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Raw results saved to: {json_path}")

if __name__ == "__main__":
    main() 