from fastapi import APIRouter, Request

from src.services.auth.serializer import LoginUserInbound, RegisterUserInbound
from src.services.auth.controller import AuthController

router = APIRouter()

@router.get("/login")
async def get_login_page(request: Request, application_id: str, redirect_uri: str):
    return AuthController.render_login_page(request, application_id, redirect_uri)

@router.post("/login")
async def authenticate_user(request: Request, payload: LoginUserInbound):
    return AuthController.login_user(request, payload)

@router.post("/register")
async def  register_user(request: Request, payload: RegisterUserInbound):
    return AuthController.register_user(request, payload)