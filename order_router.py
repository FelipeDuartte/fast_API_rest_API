from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import pegar_sessao
from schemas import SchemaPedido
from models import Pedido
# criar o router para as rotas de pedidos
order_routers = APIRouter(prefix="/orders", tags=["orders"])
# criar as rotas de pedidos
@order_routers.get("/")
async def pedidos():
    return {"message": "Lista de pedidos"}

@order_routers.post("/pedido")
async def Pedidos(pedido_schema: SchemaPedido, session: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario_id=pedido_schema.usuario_id)
    session.add(novo_pedido)
    session.commit()
    return {"message": f"Pedido criado com sucesso: {novo_pedido.id}"}