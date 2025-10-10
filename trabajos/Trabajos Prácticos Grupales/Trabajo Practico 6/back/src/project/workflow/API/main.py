from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.project.workflow.API.endpoints.compra import router_compra
from src.project.workflow.API.endpoints.monto import router_monto
from src.project.workflow.API.login.login import router_auth
from dotenv import load_dotenv
import os

load_dotenv()  

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
app = FastAPI() # LA API SE LEVANTA CON ESTE COMANDO: uvicorn src.project.workflow.API.main:app --reload

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o ["http://localhost:3000"] si usás React local
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 
app.include_router(router_compra, prefix="/compra")
app.include_router(router_monto, prefix="/monto")
app.include_router(router_auth, prefix="/auth")

@app.get("/")
def read_root():
    return {"message": "API de Gestión de Entradas - Bienvenido"}



