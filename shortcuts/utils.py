import random
import string

CODE_SIZE = 6


def generate_random_code(size: int = CODE_SIZE) -> str:
    """Generate random code of specified length containing only random letters and digits."""
    allowed_chars = string.ascii_letters + string.digits
    return "".join(random.choice(allowed_chars) for _ in range(size))
