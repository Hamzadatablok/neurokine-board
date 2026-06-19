"""
Scientific logic reused from the injury-risk-predictor project.
Deterministic, unit-tested functions the committee agents can call as tools.
"""

from typing import List


def compute_acwr(daily_loads: List[float]) -> dict:
    """Compute the Acute:Chronic Workload Ratio (ACWR) and its zone."""
    if len(daily_loads) < 7:
        raise ValueError("At least 7 days are required")

    acute = sum(daily_loads[-7:]) / 7
    chronic_window = daily_loads[-28:]
    chronic = sum(chronic_window) / len(chronic_window)

    acwr = round(acute / chronic, 2) if chronic > 0 else 0.0

    if acwr < 0.80:
        zone = "undertraining"
    elif acwr <= 1.30:
        zone = "sweet_spot"
    else:
        zone = "danger"

    return {
        "acute_load": round(acute, 1),
        "chronic_load": round(chronic, 1),
        "acwr": acwr,
        "acwr_zone": zone,
    }


def compute_risk(acwr: float, sleep: float, resting_hr: int,
                 previous_injuries: int = 0, soreness: int = 0) -> dict:
    """Combine several factors into a 0-100 risk score and its level."""
    score = 0
    factors: List[str] = []

    if acwr > 1.50:
        score += 40
        factors.append(f"Very high ACWR ({acwr})")
    elif acwr > 1.30:
        score += 25
        factors.append(f"ACWR above optimal ({acwr})")
    elif acwr < 0.80:
        score += 10
        factors.append(f"Low ACWR ({acwr})")

    if sleep < 6:
        score += 20
        factors.append(f"Insufficient sleep ({sleep}h)")

    if resting_hr > 70:
        score += 10
        factors.append(f"Elevated resting HR ({resting_hr})")

    if previous_injuries >= 2:
        score += 20
        factors.append(f"Recurrent injuries ({previous_injuries})")

    if soreness >= 7:
        score += 10
        factors.append(f"High muscle soreness ({soreness}/10)")

    score = min(score, 100)

    if score >= 70:
        level = "critical"
    elif score >= 45:
        level = "high"
    elif score >= 25:
        level = "moderate"
    else:
        level = "low"

    return {"risk_score": score, "risk_level": level, "factors": factors}


def assess_athlete(daily_loads: List[float], sleep: float, resting_hr: int,
                   previous_injuries: int = 0, soreness: int = 0) -> dict:
    """Full assessment: compute ACWR first, then feed it into the risk score.

    This guarantees the correct order (risk depends on ACWR), so the LLM
    never has to chain the two calls itself.
    """
    workload = compute_acwr(daily_loads)
    risk = compute_risk(
        acwr=workload["acwr"],
        sleep=sleep,
        resting_hr=resting_hr,
        previous_injuries=previous_injuries,
        soreness=soreness,
    )
    return {"workload": workload, "risk": risk}
