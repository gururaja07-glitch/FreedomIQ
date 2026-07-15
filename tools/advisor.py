# ==========================================
# FreedomIQ Advisor
# ==========================================

def generate_advice(summary, health, actions):

    advisor = {
        "Health": "",
        "Strengths": [],
        "Warnings": [],
        "Actions": []
    }

    # Health
    if health["Total"] >= 95:
        advisor["Health"] = "Excellent"

    elif health["Total"] >= 85:
        advisor["Health"] = "Good"

    else:
        advisor["Health"] = "Needs Improvement"

    # Strengths

    if summary["Number of Sectors"] >= 8:
        advisor["Strengths"].append(
            "Well diversified across sectors."
        )

    if summary["Cash Weight"] >= 5:
        advisor["Strengths"].append(
            "Healthy cash allocation."
        )

    if summary["Gold Weight"] >= 5:
        advisor["Strengths"].append(
            "Healthy gold allocation."
        )

    # Warnings & Actions

    if len(actions) == 0:

        advisor["Actions"].append(
            "No portfolio changes required."
        )

    else:

        for action in actions:

            advisor["Warnings"].append(
                f'{action["Type"]}: {action["Name"]}'
            )

            advisor["Actions"].append(
                f'Reduce {action["Name"]} '
                f'by {action["Excess"]:.2f}%'
            )

    return advisor