# src/dependencies/validate_app.py

from fastapi import Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.configs.enums import ApplicationStatus
from src.lib.db_session import get_db, select_first
from src.schema.schema import ApplicationModel

def validate_application_query(
    application_id: str = Query(...),
    redirect_uri: str = Query(...),
) -> tuple[ApplicationModel, str]:
    db = get_db()
    app_query = db.query(ApplicationModel).filter_by(application_id=application_id)
    app = select_first(app_query)

    if not app:
        raise HTTPException(status_code=400, detail="Invalid application_id")

    if redirect_uri not in app.redirect_uris:
        raise HTTPException(status_code=400, detail="Invalid redirect_uri")

    if app.status != ApplicationStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Application Disabled")

    return app, redirect_uri
