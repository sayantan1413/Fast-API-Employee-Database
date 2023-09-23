# app.py
from fastapi import FastAPI
import controllers.controller as controller

app = FastAPI()

# Include your routers
app.include_router(controller.router)
