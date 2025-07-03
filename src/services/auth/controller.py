from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse, JSONResponse
from starlette.templating import Jinja2Templates

from src.lib.bcrypt import hasher
from src.lib.db_session import get_db, select_first, save_new_row
from src.schema.schema import UserModel
from src.services.auth.serializer import LoginUserInbound, RegisterUserInbound
from src.configs.enums import ApplicationStatus
from src.schema.schema import SessionModel, AuthCodeModel, ApplicationModel
from src.lib.urllib import url
from uuid import uuid4
import base64


templates = Jinja2Templates(directory="templates")


class AuthController:
    @staticmethod
    def render_login_page(request: Request, payload: tuple[ApplicationModel, str]):
        application, redirect_uri = payload
        db = get_db()
        session_id = request.cookies.get("session_id")

        if session_id:
            query = db.query(SessionModel).filter(SessionModel.id == session_id)
            session: Optional[SessionModel] = select_first(query)
            if session and session.expires_at > datetime.utcnow():
                auth_code = str(uuid4())
                save_new_row(AuthCodeModel(
                    code=auth_code,
                    user_id=session.user_id,
                    application_id=application.application_id,
                    expires_at=datetime.utcnow() + timedelta(minutes=5)
                ))

                return RedirectResponse(url=url.build_redirect_url(redirect_uri, params={"authorisation_code": auth_code}))

        return templates.TemplateResponse("login.html", {
            "request": request,
            "application_id": application.application_id,
            "redirect_uri": redirect_uri
        })

    @staticmethod
    def login_user(request: Request, payload: LoginUserInbound, app_payload: tuple[ApplicationModel, str]):
        db = get_db()
        application, _ = app_payload
        query = db.query(UserModel).filter(UserModel.email == payload.email)
        existing_user: Optional[UserModel] = select_first(query)

        if not existing_user:
            raise HTTPException(status_code=404, detail="No user with given email exists")

        is_password_correct = hasher.verify_password(payload.password, existing_user.password_hash)

        if not is_password_correct:
            raise HTTPException(status_code=400, detail="Email or Password incorrect")

        new_session = SessionModel(
            user_id=existing_user.id,
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(hours=4),
            user_agent=request.headers.get("user-agent"),
            ip=request.client.host
        )
        session: SessionModel = save_new_row(new_session)

        auth_code = str(uuid4())
        save_new_row(AuthCodeModel(
            code=auth_code,
            user_id=session.user_id,
            application_id=application.application_id,
            expires_at=datetime.utcnow() + timedelta(minutes=5)
        ))

        response = JSONResponse(status_code=200, content={
            "message": "Login successful",
            "authorization_code": auth_code
        })
        response.set_cookie(key="session_id", value=session.id, httponly=True, max_age=60 * 60 * 4)
        return response

    @staticmethod
    def register_user(request: Request, payload: RegisterUserInbound, app_payload: tuple[ApplicationModel, str]):
        db = get_db()
        application, _ = app_payload
        user_query = db.query(UserModel).filter(UserModel.email == payload.email)
        existing_user:  Optional[UserModel] = select_first(user_query)

        if existing_user:
            raise HTTPException(status_code=400, detail="User with given email already exists")

        try:
            password = base64.b64decode(payload.password).decode("utf-8")
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid password encoding")
        hashed_password = hasher.hash_password(password)

        new_user = UserModel(
            email=payload.email,
            password_hash=hashed_password,
        )
        user = save_new_row(new_user)

        new_session = SessionModel(
            user_id=user.id,
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(hours=4),
            user_agent=request.headers.get("user-agent"),
            ip=request.client.host
        )
        session: SessionModel = save_new_row(new_session)

        auth_code = str(uuid4())
        save_new_row(AuthCodeModel(
            code=auth_code,
            user_id=session.user_id,
            application_id=application.application_id,
            expires_at=datetime.utcnow() + timedelta(minutes=5)
        ))

        response = JSONResponse(status_code=200, content={
            "message": "User Registered Successfully",
            "authorization_code": auth_code
        })
        response.set_cookie(key="session_id", value=session.id, httponly=True, max_age=60 * 60 * 4)
        return response