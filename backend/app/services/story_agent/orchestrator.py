import asyncio
import os
import logging
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
from base import Agent
from intake import IntakeAgent
from creative import CreativeAgent
from llm_providers import OpenAIProvider, ClaudeProvider, GrokProvider, TogetherAIProvider


# Ensure logs directory exists
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
log_filename = log_dir / f"llm_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"


PROVIDER = "together"  # Change to "openai" or "claude"

input0 = """
Story. Girl. Ball. Park. Lily 2 yrs. She got a new bouncy ball today.
"""
input1 = """
pls make a story for olivia she is 3. she just learned to put on her OWN jacket 
with the zipper! she did it all by herself before we went to the park this 
morning to feed ducks. can the story be about olivia or a girl like her getting 
ready to go out, zipping her jacket (make the zipper sound like Zzzzzzip!), 
and then having fun at the park? short and sweet please.
"""

# Optional: Set this to a string to add a custom comment at the top of the log file for this run.
USER_RUN_COMMENT = "new prompt design for intake agent"
if USER_RUN_COMMENT:
    RUN_COMMENT = f"""
# =============================================
# USER COMMENT:
# {USER_RUN_COMMENT}
# =============================================
"""
else:
    RUN_COMMENT = f"""
# =============================================
# LLM RUN - {datetime.now().isoformat()}
# Input: 
# {input1}
# Main Creative Brief (truncated):
# {(' '.join(line.strip() for line in str(creative_brief).splitlines() if line)[:300])}
# =============================================
"""

# Write the run comment at the top of the log file
with open(log_filename, "w") as f:
    f.write(RUN_COMMENT)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler(log_filename, mode='a'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AgentNode:
    def __init__(
        self,
        name,
        agent_cls,
        provider_name,
        dependencies=None,
        agent_kwargs=None,
        provider_kwargs=None,
        run_kwargs=None,  # For runtime/step-specific kwargs
    ):
        self.name = name
        self.agent_cls = agent_cls
        self.provider_name = provider_name
        self.dependencies = dependencies or []
        self.agent_kwargs = agent_kwargs or {}
        self.provider_kwargs = provider_kwargs or {}
        self.run_kwargs = run_kwargs or {}
        self.agent = None
        self.result = None

class Orchestrator:
    def __init__(self, nodes):
        self.nodes = {node.name: node for node in nodes}
        self.execution_order = self._topological_sort()

    def _get_provider(self, provider_name, provider_kwargs):
        if provider_name == "openai":
            return OpenAIProvider(api_key=os.getenv("OPENAI_API_KEY"), **provider_kwargs)
        elif provider_name == "claude":
            return ClaudeProvider(api_key=os.getenv("CLAUDE_API_KEY"), **provider_kwargs)
        elif provider_name == "grok":
            return GrokProvider(api_key=os.getenv("GROK_API_KEY"), **provider_kwargs)
        elif provider_name == "together":
            return TogetherAIProvider(api_key=os.getenv("TOGETHER_API_KEY"), **provider_kwargs)
        else:
            raise ValueError(f"Unknown provider: {provider_name}")

    def _topological_sort(self):
        return [node.name for node in self.nodes.values()]

    async def run(self, initial_artifacts):
        """
        Executes the DAG of agent nodes in topological order, passing artifacts (outputs) from node to node.

        Artifact Naming & Passing:
        -------------------------
        - Each agent node's output is stored in the artifacts dict under its node name (e.g., 'intake', 'creative').
        - When an agent has dependencies, the orchestrator passes the output of each dependency as a keyword argument to the agent, using the dependency's node name as the kwarg name.
        - If an agent returns a dict, the entire dict is passed as the kwarg value (e.g., 'intake': {...}).
        - Downstream agents should accept kwargs named after their dependencies and extract the needed values.

        Example:
        --------
        Suppose you have two agents:
            - IntakeAgent (node name: 'intake')
            - CreativeAgent (node name: 'creative', depends on 'intake')

        The DAG setup:
            nodes = [
                AgentNode('intake', IntakeAgent, 'openai', run_kwargs={'parental_input': input1}),
                AgentNode('creative', CreativeAgent, 'together', dependencies=['intake'])
            ]
            orchestrator = Orchestrator(nodes)
            results = await orchestrator.run(initial_artifacts={})

        Execution flow:
            1. IntakeAgent runs first, receives 'parental_input', and produces a creative brief (md).
            2. CreativeAgent runs next, and receives the output of IntakeAgent as a kwarg: creative_agent(intake=<intake_result>)
            3. CreativeAgent extracts what it needs from 'intake' and produces its own output.

        This pattern generalizes to any number of agents and dependencies.
        
        ---
        initial_artifacts usage:
        -----------------------
        Use initial_artifacts to inject the output of a dependency that is not produced by a previous agent in the current run. This is useful for:
        - Resuming or testing a pipeline from a specific step (e.g., start from 'creative' with a precomputed 'intake' result)
        - Bypassing expensive or unnecessary steps by providing their expected outputs directly
        - Unit testing downstream agents with mock or saved artifacts
        - Handling complex DAGs where some nodes depend on external data

        | Use Case                        | How to Provide Input                |
        |----------------------------------|-------------------------------------|
        | First node’s input               | run_kwargs in AgentNode             |
        | Downstream dependency injection  | initial_artifacts in run()          |
        | Skipping/overriding a node       | initial_artifacts in run()          |
        | Testing downstream agents        | initial_artifacts in run()          |

        Example for resuming/testing:
            saved_brief = "...markdown creative brief..."
            nodes = [
                AgentNode("creative", CreativeAgent, "together", dependencies=["intake"]),
                AgentNode("story", StoryAgent, "openai", dependencies=["creative"]),
            ]
            orchestrator = Orchestrator(nodes)
            result = await orchestrator.run(initial_artifacts={"intake": saved_brief})
        """
        artifacts = initial_artifacts.copy()
        print("Execution order:", self.execution_order)
        for node_name in self.execution_order:
            node = self.nodes[node_name]
            provider = self._get_provider(node.provider_name, node.provider_kwargs)
            node.agent = node.agent_cls(provider, **node.agent_kwargs)

            # Log the model name
            model_name = getattr(provider, "model", None)
            logger.info(f"========== {node_name.upper()} MODEL ==========")
            logger.info(model_name if model_name else "Unknown model")

            # Gather input artifacts from dependencies
            input_artifacts = {dep: self.nodes[dep].result for dep in node.dependencies}
            # Merge run_kwargs with input_artifacts for agent call
            agent_input = {**input_artifacts, **node.run_kwargs}

            # Get and log system/user prompts
            if hasattr(node.agent, "get_formatted_prompts"):
                try:
                    system_prompt, user_prompt = node.agent.get_formatted_prompts(**agent_input)
                    logger.info(f"========== {node_name.upper()} SYSTEM PROMPT ==========")
                    logger.info(system_prompt)
                    logger.info(f"========== {node_name.upper()} USER PROMPT ==========")
                    logger.info(user_prompt)
                except Exception as e:
                    logger.warning(f"Could not get prompts for {node_name}: {e}")

            # Run the agent and log result
            node.result = await node.agent(**agent_input)
            artifacts[node_name] = node.result
            logger.info(f"========== {node_name.upper()} RESULT ==========")
            logger.info(node.result)

        return artifacts

async def main():

    nodes = [
        AgentNode(
            "intake",
            IntakeAgent,
            "openai",
            run_kwargs={"parental_input": input1},
        ),
        AgentNode(
            "creative",
            CreativeAgent,
            "together",
            dependencies=["intake"],
            # agent_kwargs={"creativity_level": "high"},
            # provider_kwargs={"model": "together-llama"},
        ),
    ]
    orchestrator = Orchestrator(nodes)
    result = await orchestrator.run(initial_artifacts={"intake": {"creative_brief_md": "test"}})

if __name__ == "__main__":
    asyncio.run(main())
