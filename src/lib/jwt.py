import jwt
from typing import Dict
from datetime import datetime, timedelta
from src.configs.env import get_settings

configs = get_settings()

class JWTManager:
    def __init__(
        self,
        algorithm: str = "RS256"
    ):
        self.algorithm = algorithm

    def generate_token(self, private_key: str, payload: Dict, expires_in: int = 3600) -> str:
        """
        Generate a JWT using the private key.
        """
        if "\\n" in private_key:
            private_key = private_key.replace("\\n", "\n")

        print(private_key)
        if not private_key:
            raise ValueError("Private key not provided. Cannot generate token.")

        payload = {
            **payload,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(seconds=expires_in)
        }

        token = jwt.encode(payload, private_key, algorithm=self.algorithm)
        return token

jwt_manager = JWTManager()