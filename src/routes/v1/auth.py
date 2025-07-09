from fastapi import APIRouter, Request, Depends
from fastapi.params import Header

from src.dependency.valid_app import validate_application_query
from src.schema.schema import ApplicationModel
from src.services.auth.serializer import LoginUserInbound, RegisterUserInbound
from src.services.auth.controller import AuthController

router = APIRouter()


@router.get("/login")
async def get_login_page(request: Request, payload: tuple[ApplicationModel, str] = Depends(validate_application_query)):
    return AuthController.render_login_page(request, payload)


@router.post("/login")
async def authenticate_user(request: Request, payload: LoginUserInbound, app_payload: tuple[ApplicationModel, str] = Depends(validate_application_query)):
    return AuthController.login_user(request, payload, app_payload)


@router.post("/register")
async def register_user(request: Request, payload: RegisterUserInbound, app_payload: tuple[ApplicationModel, str] = Depends(validate_application_query)):
    return AuthController.register_user(request, payload, app_payload)

@router.get("/token")
async def get_login_page(request: Request, auth_code: str, authorization: str = Header(..., alias="Authorization")):
    return AuthController.get_user_tokens(request, auth_code, authorization)