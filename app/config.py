MODEL_NAME = "facebook/bart-large-mnli"

CANDIDATE_LABELS = [
    "Sachliche Kritik",
    "Zustimmung",
    "Sarkasmus oder Ironie",
    "Off-Topic",
    "Empörung oder Rant",
    "Desinformation oder Verschwörung",
]

MAX_BATCH_SIZE = 8
BATCH_TIMEOUT_SECONDS = 0.2
