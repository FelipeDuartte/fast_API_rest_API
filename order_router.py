from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import SchemaPedido
from models import Pedido, Usuario
# criar o router para as rotas de pedidos
order_routers = APIRouter(prefix="/orders", tags=["orders"], dependencies=[Depends(verificar_token)])
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

@order_routers.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado!")
    if not usuario.admin and usuario.id != pedido.usuario_id:
        raise HTTPException(status_code=401, detail="Você não esta autorizado a alterar esse pedido!")
    pedido.status = "CANCELADO"
    session.commit()
    return {
        "Menssagem": f"pedido {pedido.id} cancelado com sucesso",
        "Pedido": pedido
    }