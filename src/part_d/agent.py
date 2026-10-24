import json
import pandas as pd

scenarios = pd.read_csv(
    "data/raw/agent_scenarios.csv"
)

runs = []
ledger = []

for _, row in scenarios.iterrows():

    runs.append({
        "scenario_id":
            row["scenario_id"],
        "action":
            "search_policy",
        "status":
            "completed"
    })

    query = str(
        row.get(
            "query",
            ""
        )
    ).lower()

    if "refund" in query:

        ledger.append({
            "scenario_id":
                row["scenario_id"],
            "refund_amount":
                100
        })

with open(
    "outputs/agent_runs.jsonl",
    "w"
) as f:

    for record in runs:

        f.write(
            json.dumps(record)
            + "\n"
        )

with open(
    "outputs/refund_ledger.jsonl",
    "w"
) as f:

    for record in ledger:

        f.write(
            json.dumps(record)
            + "\n"
        )

print(
    "Agent Runs:",
    len(runs)
)

print(
    "Refund Entries:",
    len(ledger)
)