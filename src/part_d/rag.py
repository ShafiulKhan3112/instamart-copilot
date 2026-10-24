import os

policy_docs = []

for file in os.listdir("data/policies"):

    path = os.path.join(
        "data/policies",
        file
    )

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        text = f.read()

    policy_docs.append({
        "file": file,
        "length": len(text)
    })

print(
    "Policies Loaded:",
    len(policy_docs)
)

for doc in policy_docs:

    print(
        doc["file"],
        doc["length"]
    )