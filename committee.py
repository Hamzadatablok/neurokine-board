"""
Assemble the four agents into a discussing committee.

SelectorGroupChat acts as an intelligent chair: after each turn it reads the
conversation and picks the most relevant agent to speak next — just like a
chair running a multidisciplinary medical board.

The discussion stops when the Safety_Auditor says "APPROVED" or after a
maximum number of messages (a safety cap against infinite loops).
"""

from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination

from agents import (
    model_client,
    kinesiology_expert,
    sports_psychologist,
    data_analyst,
    safety_auditor,
)


def build_committee() -> SelectorGroupChat:
    # Stop when the auditor approves, OR after 20 messages (whichever comes first)
    termination = TextMentionTermination("APPROVED") | MaxMessageTermination(20)

    return SelectorGroupChat(
        participants=[
            kinesiology_expert,
            sports_psychologist,
            data_analyst,
            safety_auditor,
        ],
        model_client=model_client,   # the chair uses the LLM to pick the next speaker
        termination_condition=termination,
    )
