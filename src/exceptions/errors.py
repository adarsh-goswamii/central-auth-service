from typing import Optional, Dict

class JWTValidationResult:
    def __init__(self, valid: bool, payload: Optional[Dict] = None, error: Optional[str] = None):
        self.valid = valid
        self.payload = payload
        self.error = error
