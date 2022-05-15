
from fastapi import FastAPI, Header
from .api import router as api_router


app = FastAPI()

app.include_router(api_router)
