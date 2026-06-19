"""
NeuroKine Board — the four committee agents (AutoGen v0.4 / AgentChat).

Each agent is an AssistantAgent with a clear system_message defining its
specialty. The Kinesiology expert is also given the scientific tools so the
committee's reasoning is grounded in real, deterministic calculations.
"""

import os
from dotenv import load_dotenv

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

from science import assess_athlete

load_dotenv()

# Shared model client — routed through OpenRouter.
# model_info is required because OpenRouter models are not in AutoGen's registry.
model_client = OpenAIChatCompletionClient(
    model=os.getenv("MODEL_NAME", "openai/gpt-4o-mini"),
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model_info={
        "family": "gpt-4o",
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "structured_output": True,
    },
)


# ---------- Agent 1: Kinesiology Expert (has the science tools) ----------
kinesiology_expert = AssistantAgent(
    name="Kinesiology_Expert",
    model_client=model_client,
    tools=[assess_athlete],
    system_message=(
        "You are a kinesiology and biomechanics expert. You analyze movement, "
        "injury mechanism and training load. When workload data is provided, "
        "ALWAYS call the assess_athlete tool to ground your analysis in real "
        "numbers (it returns both the ACWR workload and the risk) — never guess. "
        "Share your findings clearly with the committee."
    ),
)


# ---------- Agent 2: Sports Psychologist ----------
sports_psychologist = AssistantAgent(
    name="Sports_Psychologist",
    model_client=model_client,
    system_message=(
        "You are a sports psychologist. You assess the athlete's mental state: "
        "fear of re-injury, motivation, stress and readiness to return. "
        "Contribute the psychological perspective to the committee discussion."
    ),
)


# ---------- Agent 3: Data & Biomechanics Analyst ----------
data_analyst = AssistantAgent(
    name="Data_Analyst",
    model_client=model_client,
    system_message=(
        "You are a sports data and biomechanics analyst. You interpret numeric "
        "data (VO2 max, heart rate, joint angles, ACWR) and turn it into clear "
        "insights for the committee. Reference the numbers explicitly."
    ),
)


# ---------- Agent 4: Safety & Ethics Auditor ----------
safety_auditor = AssistantAgent(
    name="Safety_Auditor",
    model_client=model_client,
    system_message=(
        "You are a safety and ethics auditor. You review the proposed protocol "
        "to ensure it does NOT cause harm and respects medical ethics. "
        "Once the committee has agreed on a safe, unified protocol, reply with "
        "the final protocol followed by the word APPROVED."
    ),
)
