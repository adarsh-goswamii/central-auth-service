from fastapi import APIRouter, Request

from src.services.auth.controller import AuthController

router = APIRouter()

@router.get("/login")
async def add_application(request: Request, application_id: str, redirect_uri: str):
    return AuthController.render_login_page(request, application_id, redirect_uri)