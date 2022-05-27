
from fastapi import FastAPI, Header
from .api import router as api_router


app = FastAPI(title="Light API", version='0.1.1')

app.include_router(api_router)
