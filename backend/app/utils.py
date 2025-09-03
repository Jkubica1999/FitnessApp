from passlib.context import CryptContext

# Configure passlib to use bcrypt (a secure hashing algorithm for passwords)
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain_password: str) -> str:
    """
    Turn a plain password into a secure hash.
    - Adds a random salt automatically.
    - Slow by design (resists brute force attacks).
    """
    return _pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Check if a plain password matches the stored hash.
    Returns True if valid, False otherwise.
    """
    return _pwd_context.verify(plain_password, hashed_password)