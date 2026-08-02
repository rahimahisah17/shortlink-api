import shortuuid
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import models
from app.database import Base, SessionLocal, engine


app = FastAPI(title="ShortLink API")

Base.metadata.create_all(bind=engine)


class URLRequest(BaseModel):
    url: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/shorten")
def shorten_url(request: URLRequest, db: Session = Depends(get_db)):
    short_link = models.ShortLink(
        original_url=request.url,
        short_code=shortuuid.uuid()[:6],
    )

    db.add(short_link)
    db.commit()
    db.refresh(short_link)

    return {
        "original_url": short_link.original_url,
        "short_code": short_link.short_code,
    }


@app.get("/{short_code}")
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    short_link = (
        db.query(models.ShortLink)
        .filter(models.ShortLink.short_code == short_code)
        .first()
    )

    if not short_link:
        raise HTTPException(status_code=404, detail="Short link not found")

    return RedirectResponse(url=short_link.original_url)