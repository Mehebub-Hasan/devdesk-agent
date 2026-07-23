import os
from pathlib import Path

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parents[1]

load_dotenv(BACKEND_DIR / ".env")

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-v4-flash")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
USE_DEEPSEEK = os.getenv("USE_DEEPSEEK", "false").lower() == "true"


def deepseek_ready() -> bool:
    """
    True only when DeepSeek is both enabled and usable.

    We gate on the key as well as the flag because a flag set to true with an
    empty key would otherwise attempt a real API call and fail with a 502.
    Callers use this to fall back to the local answer instead.
    """

    return USE_DEEPSEEK and bool(DEEPSEEK_API_KEY)
