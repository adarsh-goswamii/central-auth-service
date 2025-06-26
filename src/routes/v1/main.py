from fastapi import APIRouter
from src.routes.v1 import auth

api_router = APIRouter()

api_router.include_router(auth.router, prefix='/v1/oauth', tags=["Oauth"])