# CrewAI Multi-Agent Story Generation System

## Overview

This implementation uses **CrewAI**, a multi-agent framework, to create personalized children's stories through collaborative AI agents. Each agent has a specialized role in the story creation process, working together to produce engaging, age-appropriate content.

## Architecture

### 🤖 Agent Roles

Our system uses specialized agents that collaborate to create stories:

#### Core Agents
1. **Story Analyst** - Analyzes images and user inputs to extract story elements
2. **Story Writer** - Creates the main story content with age-appropriate language
3. **Story Enhancer** - Adds emotional depth and sensory details
4. **Visual Coordinator** - Plans visual elements for each story segment
5. **Quality Reviewer** - Reviews and refines the final story

#### Specialized Agents
1. **Adventure Story Specialist** - Creates exciting adventure narratives
2. **Friendship Story Specialist** - Focuses on social connections and kindness
3. **Educational Story Specialist** - Integrates learning concepts seamlessly
4. **Bedtime Story Specialist** - Creates calming, peaceful stories
5. **Cultural Story Specialist** - Celebrates diversity and different cultures
6. **Interactive Story Designer** - Adds participation opportunities
7. **Character Developer** - Creates memorable, relatable characters
8. **Dialogue Specialist** - Writes natural, engaging conversations
9. **World Builder** - Creates immersive story settings
10. **Emotion Specialist** - Integrates emotional learning

### 🏗️ System Structure

```
backend/app/
├── models/
│   └── story_models.py          # Pydantic models for data structures
├── services/
│   ├── crew_story_generator.py  # Basic CrewAI implementation
│   ├── enhanced_crew_generator.py # Advanced dynamic agent selection
│   └── specialized_agents.py    # Specialized agent factory
├── routes/
│   └── crew_story_routes.py     # FastAPI endpoints
└── examples/
    └── crewai_example.py        # Usage examples
```

## Features

### 🎯 Dynamic Agent Selection
The system intelligently selects specialized agents based on:
- **Story theme** (adventure, friendship, educational, etc.)
- **Target age group** (3-5, 4-6, 6-8)
- **Story length** (short, medium, long)
- **User instructions and context**

### 🔄 Workflow Patterns
- **Sequential Processing** - Agents work in order, building on previous results
- **Hierarchical Processing** - Manager agent coordinates specialized agents
- **Retry Logic** - Automatic retry on failures with exponential backoff

### 📊 Performance Monitoring
- Execution time tracking
- Success rate analysis
- Agent performance metrics
- Detailed execution history

## Quick Start

### 1. Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY="your-openai-api-key"

# Disable CrewAI telemetry (recommended for privacy)
export CREWAI_TELEMETRY_OPT_OUT=true
export OTEL_SDK_DISABLED=true
```

### 2. Disable Telemetry (Privacy)

CrewAI collects telemetry data by default. To disable it:

**Option 1: Environment Variables**
```bash
export CREWAI_TELEMETRY_OPT_OUT=true
export OTEL_SDK_DISABLED=true
export DO_NOT_TRACK=1
```

**Option 2: In Your Code**
```python
import os
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"
```

**Option 3: Using Our Utility**
```python
from app.utils.telemetry import disable_crewai_telemetry, get_telemetry_status

# Disable telemetry
disable_crewai_telemetry()

# Check status
status = get_telemetry_status()
print(f"Telemetry disabled: {status['telemetry_disabled']}")
```

### 3. Basic Usage

```python
from app.models.story_models import StoryRequest, TargetAge, StoryLength
from app.services.enhanced_crew_generator import EnhancedCrewStoryGenerator

# Create a story request
story_request = StoryRequest(
    text_instructions="Create a story about a brave little rabbit",
    target_age=TargetAge.TODDLER,
    story_length=StoryLength.SHORT,
    theme="adventure"
)

# Generate story
generator = EnhancedCrewStoryGenerator()
result = await generator.generate_story_enhanced(story_request)

if result.success:
    print(f"Generated: {result.final_result.title}")
    print(f"Segments: {len(result.final_result.segments)}")
```

### 4. API Usage

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

#### Generate Basic Story
```bash
curl -X POST "http://localhost:8000/crew-stories/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "text_instructions": "A story about friendship",
    "target_age": "3-5",
    "story_length": "short",
    "theme": "friendship"
  }'
```

#### Generate Enhanced Story
```bash
curl -X POST "http://localhost:8000/crew-stories/generate-enhanced" \
  -H "Content-Type: application/json" \
  -d '{
    "text_instructions": "An educational story about counting",
    "target_age": "4-6", 
    "story_length": "medium",
    "theme": "educational"
  }'
```

## API Endpoints

### Story Generation
- `POST /crew-stories/generate` - Basic story generation
- `POST /crew-stories/generate-enhanced` - Enhanced with dynamic agents
- `POST /crew-stories/generate-by-theme/{theme}` - Theme-specific generation
- `POST /crew-stories/generate-async` - Asynchronous generation

### Monitoring & Management
- `GET /crew-stories/status/{task_id}` - Check async task status
- `GET /crew-stories/metrics` - Performance metrics
- `GET /crew-stories/execution-history` - Recent execution history
- `GET /crew-stories/available-themes` - List supported themes

### Configuration
- `GET /crew-stories/config` - Get current configuration
- `POST /crew-stories/config` - Update configuration

### Telemetry & Privacy
- `GET /crew-stories/telemetry-status` - Check telemetry configuration status

## Configuration Options

### StoryGenerationConfig

```python
config = StoryGenerationConfig(
    model_name="gpt-4",           # LLM model to use
    temperature=0.7,              # Creativity level (0.0-1.0)
    max_tokens=2000,              # Max tokens per agent
    enable_verbose_logging=True,   # Detailed logging
    process_type="sequential",     # sequential or hierarchical
    max_retry_attempts=3,         # Retry failed generations
    min_story_segments=3,         # Minimum story length
    max_story_segments=15         # Maximum story length
)

generator = EnhancedCrewStoryGenerator(config)
```

## Agent Team Compositions

### Adventure Stories
- Adventure Story Specialist
- Character Developer  
- World Builder
- Interactive Story Designer

### Friendship Stories
- Friendship Story Specialist
- Character Developer
- Dialogue Specialist
- Emotion Specialist

### Educational Stories
- Educational Story Specialist
- Interactive Story Designer
- Character Developer

### Bedtime Stories
- Bedtime Story Specialist
- World Builder
- Emotion Specialist

### Cultural Stories
- Cultural Story Specialist
- Character Developer
- World Builder
- Dialogue Specialist

## Story Output Structure

### StoryResponse
```json
{
  "title": "The Brave Little Rabbit",
  "segments": [
    {
      "segment_id": 1,
      "text": "Once upon a time, there lived a brave little rabbit named Hopscotch.",
      "visual_description": {
        "scene_description": "A cozy burrow with a small rabbit wearing a tiny red cape",
        "composition": "Close-up of the rabbit in the center",
        "color_palette": ["warm brown", "bright red", "golden yellow"],
        "mood": "warm and inviting"
      },
      "duration_seconds": 30,
      "interactive_elements": ["Can you hop like Hopscotch?"],
      "emotional_tone": "cheerful and excited"
    }
  ],
  "total_duration": 240,
  "summary": "A brave rabbit goes on an adventure and learns about courage",
  "themes": ["courage", "friendship", "adventure"],
  "characters": ["Hopscotch the Rabbit", "Wise Owl", "Forest Friends"]
}
```

## Best Practices

### 1. Agent Selection
- Use specialized agents for targeted content types
- Combine complementary agents (e.g., Character Developer + Dialogue Specialist)
- Consider target age when selecting interactive elements

### 2. Configuration Tuning
- **High creativity** (temperature 0.8-0.9) for unique, imaginative stories
- **Low creativity** (temperature 0.3-0.5) for consistent, structured content
- **Medium creativity** (temperature 0.6-0.7) for balanced results

### 3. Performance Optimization
- Use async generation for long-running requests
- Monitor execution times and adjust timeouts
- Implement caching for repeated requests

### 4. Error Handling
- Always check `result.success` before using story data
- Implement fallback mechanisms for failed generations
- Log errors for debugging and improvement

## Monitoring & Analytics

### Performance Metrics
```python
metrics = generator.get_performance_metrics()
print(f"Success rate: {metrics['success_rate']:.1f}%")
print(f"Avg execution time: {metrics['average_execution_time']:.2f}s")
```

### Execution History
```python
history = generator.get_execution_history()
for execution in history[-5:]:  # Last 5 executions
    print(f"Success: {execution.success}, Time: {execution.total_execution_time:.2f}s")
```

## Extending the System

### Adding New Agents

1. **Create the Agent**
```python
def create_music_story_writer(self) -> Agent:
    return Agent(
        role="Music Story Specialist",
        goal="Create stories that incorporate musical elements",
        backstory="You specialize in stories about music, rhythm, and sound...",
        llm=self.llm
    )
```

2. **Add to Agent Factory**
```python
# Add method to SpecializedAgentFactory
def create_music_story_writer(self) -> Agent:
    # Implementation here
    pass
```

3. **Update Team Builder**
```python
def _build_music_team(self) -> list:
    return [
        self.factory.create_music_story_writer(),
        self.factory.create_character_developer(),
        self.factory.create_interactive_story_designer()
    ]
```

### Custom Workflows

```python
# Custom task creation
def create_custom_tasks(self, story_request: StoryRequest) -> List[Task]:
    tasks = []
    
    # Add custom task logic here
    custom_task = Task(
        description="Custom task description",
        agent=selected_agent,
        expected_output="Expected output format"
    )
    tasks.append(custom_task)
    
    return tasks
```

## Troubleshooting

### Common Issues

1. **API Key Errors**
   - Ensure `OPENAI_API_KEY` environment variable is set
   - Check API key permissions and billing status

2. **Generation Failures**
   - Review agent prompts for clarity
   - Adjust temperature settings
   - Check token limits

3. **Performance Issues**
   - Monitor execution times
   - Consider reducing story complexity
   - Use async generation for long requests

4. **Agent Coordination Issues**
   - Review task dependencies
   - Ensure clear expected outputs
   - Check agent role definitions

### Debug Mode

Enable verbose logging for detailed execution information:
```python
config = StoryGenerationConfig(enable_verbose_logging=True)
generator = EnhancedCrewStoryGenerator(config)
```

## Contributing

When contributing to the CrewAI system:

1. **Test New Agents** - Ensure they work well with existing agents
2. **Update Documentation** - Document new features and configurations
3. **Add Examples** - Provide usage examples for new functionality
4. **Monitor Performance** - Check impact on execution time and success rates

## Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

---

This CrewAI implementation provides a flexible, scalable foundation for generating personalized children's stories using collaborative AI agents. The system can be easily extended with new agents, workflows, and capabilities as your requirements evolve. 