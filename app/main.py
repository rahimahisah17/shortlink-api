from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="ShortLink API")


class URLRequest(BaseModel):
    url: str


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/shorten")
def shorten_url(request: URLRequest):
    return {
        "original_url": request.url,
        "short_url": "https://short.ly/demo"
    }