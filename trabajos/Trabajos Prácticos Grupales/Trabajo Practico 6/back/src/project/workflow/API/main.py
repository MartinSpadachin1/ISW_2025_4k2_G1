from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.project.workflow.API.endpoints.compra import router_compra
from src.project.workflow.API.endpoints.monto import router_monto
from src.project.workflow.API.login.login import router_auth
from src.project.workflow.API.endpoints.pago import router_pago

from sqlmodel import Session
from src.common.persistance.database import create_db_and_tables
from src.project.entities import Reserva, Visitante
from src.common.persistance.models import Reserva as ReservaModel, Visitante as VisitanteModel
from contextlib import asynccontextmanager
from src.project.workflow.API.register.register import router_register


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando la aplicación...")
    create_db_and_tables()
    yield
    print("Cerrando la aplicación...")


app = FastAPI(lifespan=lifespan) # LA API SE LEVANTA CON ESTE COMANDO: uvicorn src.project.workflow.API.main:app --reload

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
app.include_router(router_register, prefix="/user")
app.include_router(router_pago, prefix="/pago")

@app.get("/")
def read_root():
    return {"message": "API de Gestión de Entradas - Bienvenido"}



