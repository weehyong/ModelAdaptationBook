"""Chapter 4: In-Context Learning and Few-Shot Adaptation."""

DEFAULT_MODEL_NAME = "Qwen/Qwen3-4B-Instruct-2507"

CATEGORIES = [
    "billing",
    "login",
    "integrations",
    "mobile",
    "performance",
    "data_export",
    "api",
    "security",
    "onboarding",
    "feature_request",
    "bug_report",
    "other",
]

DEFAULT_SYSTEM_INSTRUCTION = (
    "You are a support ticket classifier. Read the ticket and respond with "
    "exactly one category from this list: " + ", ".join(CATEGORIES) + ". "
    "Respond with the category only."
)
