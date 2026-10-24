import pandas as pd
import re

tickets = pd.read_csv(
    "data/raw/tickets.csv",
    keep_default_na=False
)

EMAIL_PATTERN = r"[\w.+-]+@[\w-]+\.[\w.]+"
PHONE_PATTERN = r"\b[6-9]\d{9}\b"
ORDER_PATTERN = r"ORD-\d{6}"

def redact(text):

    text = str(text)

    text = re.sub(
        EMAIL_PATTERN,
        "[EMAIL]",
        text
    )

    text = re.sub(
        PHONE_PATTERN,
        "[PHONE]",
        text
    )

    text = re.sub(
        ORDER_PATTERN,
        "[ORDER_ID]",
        text
    )

    return text


tickets["redacted_text"] = (
    tickets["text"]
    .apply(redact)
)

email_count = (
    tickets["text"]
    .str.count(
        EMAIL_PATTERN
    )
    .sum()
)

phone_count = (
    tickets["text"]
    .str.count(
        PHONE_PATTERN
    )
    .sum()
)

order_count = (
    tickets["text"]
    .str.count(
        ORDER_PATTERN
    )
    .sum()
)

print("Emails:", email_count)
print("Phones:", phone_count)
print("Orders:", order_count)

print(
    "Total:",
    email_count +
    phone_count +
    order_count
)
# ---------------- GUARDRAILS ----------------

def classify_ticket(text):

    text = str(text).lower()

    if len(text.strip()) == 0:
        return "skipped_empty"

    if len(text) > 1000:
        return "flagged_long"

    if "refund" in text:
        return "refund"

    if "payment" in text:
        return "payment"

    if "delivery" in text:
        return "delivery"

    if "privacy" in text:
        return "privacy"

    return "other"


tickets["category"] = (
    tickets["redacted_text"]
    .apply(classify_ticket)
)

print("\nCATEGORY COUNTS")

print(
    tickets["category"]
    .value_counts()
)

tickets.to_csv(
    "outputs/triage_results.csv",
    index=False
)

print(
    "\ntriage_results.csv saved"
)
# ---------------- BUDGET DEMO ----------------

budget_demo = tickets[
    ["ticket_id", "category"]
].copy()

budget_demo["estimated_tokens"] = 120

budget_demo["estimated_cost"] = (
    budget_demo["estimated_tokens"]
    * 0.00001
)

budget_demo.to_csv(
    "outputs/triage_budget_demo.csv",
    index=False
)

print(
    "\ntriage_budget_demo.csv saved"
)

print(
    budget_demo.head()
)