from fastapi import FastAPI
from dotenv import load_dotenv
from passlib.context import CryptContext
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEYS")

app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from auth_router import auth_routers
from order_router import order_routers

app.include_router(auth_routers)
app.include_router(order_routers)


# Para executar no terminal: uvicorn main:app --reload
# rest API:
# GET /orders -> leitura/pegar
# POST /orders -> criar/enviar
# PUT /orders/{id} -> editar/atualizar
# DELETE /orders/{id} -> deletar
