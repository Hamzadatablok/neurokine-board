"""
NeuroKine Board — entry point.

You act as the Admin: you present a patient/athlete case, and the four-agent
committee discusses it in a dynamic group chat until they agree on a safe,
unified rehabilitation / training protocol.

Run:  python main.py
"""

import asyncio

from autogen_agentchat.ui import Console
from committee import build_committee


# The case you (the Admin) bring to the committee.
PATIENT_CASE = """
Patient case for the committee to discuss:

- Name: Yassine, 24-year-old professional football player.
- Injury: returning from an ACL reconstruction 5 months ago.
- Training loads (last 28 days, RPE x minutes):
  [300, 280, 0, 320, 290, 350, 0,
   310, 300, 0, 330, 280, 360, 0,
   320, 310, 0, 340, 300, 370, 0,
   480, 520, 450, 600, 500, 650, 80]
- avg_sleep_hours: 5.5
- resting_hr: 74
- previous_injuries: 2
- soreness (1-10): 8
- The player is anxious and afraid of re-injury, but highly motivated to
  return before an important match in 3 weeks.

Discuss and agree on a unified return-to-play protocol.
The Kinesiology_Expert should use the tools to compute ACWR and risk first.
"""


async def main() -> None:
    committee = build_committee()
    # Console streams the whole discussion to the terminal as it happens.
    await Console(committee.run_stream(task=PATIENT_CASE))


if __name__ == "__main__":
    asyncio.run(main())
