import os
from dotenv import load_dotenv

load_dotenv()

# A fallback value for development only.
DEFAULT_SECRET = "TO_BE_CHANGED"

# Read values from environment if present; otherwise, use safe defaults for dev.
SECRET_KEY = os.getenv("JWT_SECRET", DEFAULT_SECRET)
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))
