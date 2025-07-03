from pydantic import BaseModel

class LoginUserInbound(BaseModel):
    email: str
    password: str

class RegisterUserInbound(BaseModel):
    email: str
    password: str