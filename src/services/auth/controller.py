from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from src.configs.enums import ApplicationStatus
from src.lib.db_session import get_db, save_new_row, select_first
from src.schema.schema import SessionModel, AuthCodeModel, ApplicationModel
from uuid import uuid4

from src.lib.urllib import url

templates = Jinja2Templates(directory="templates")


class AuthController:
    @staticmethod
    def render_login_page(request: Request, application_id: str, redirect_uri: str):
        session_id = request.cookies.get("session_id")
        db = get_db()

        query = db.query(ApplicationModel).filter(ApplicationModel.application_id == application_id)
        application: Optional[ApplicationModel] = select_first(query)
        if not application or application.status != ApplicationStatus.ACTIVE:
            raise HTTPException(status_code=400, detail="Invalid application_id")

        if url.strip_query_params(redirect_uri) not in application.redirect_uris:
            raise HTTPException(status_code=400, detail="Invalid redirect uri")

        if session_id:
            query = db.query(SessionModel).filter(SessionModel.id == session_id).first()
            session: Optional[SessionModel] = select_first(query)
            if session and session.expires_at > datetime.utcnow():
                auth_code = str(uuid4())
                save_new_row(AuthCodeModel(
                    code=auth_code,
                    user_id=session.user_id,
                    application_id=application_id,
                    expires_at=datetime.utcnow() + timedelta(minutes=5)
                ))

                return RedirectResponse(url=url.build_redirect_url(redirect_uri, params={"authorisation_code": auth_code}))

        return templates.TemplateResponse("login.html", {
            "request": request,
            "application_id": application_id,
            "redirect_uri": redirect_uri
        })
