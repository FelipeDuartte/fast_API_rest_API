from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import SchemaPedido, SchemaItemPedido, ResponseSchemaPedidos
from models import Pedido, Usuario, ItensPedido
from typing import List
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

@order_routers.get("/list")
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não esta autorizado a fazer essa alteração!")
    else:
         pedidos = session.query(Pedido).all()
         return {
             "pedidos": pedidos
         }
    
@order_routers.post("/pedido/adicionar-pedido/{id_pedido}")
async def AdicionarPedido(id_pedido: int,item_pedido_schema: SchemaItemPedido, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=401, detail="Pedido não existente")
    if not usuario.admin and usuario.id != pedido.usuario_id:
        raise HTTPException(status_code=400, detail="Você não esta autorizado a fazer essa alteração!")
    item_pedido = ItensPedido(item_pedido_schema.quantidade, item_pedido_schema.sabor, item_pedido_schema.tamanho, item_pedido_schema.preco_unitario, id_pedido)
    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        "Messagem": "pedido adicionado com sucesso",
        "item_id": item_pedido.id,
        "item_preco": pedido.preco
    }

@order_routers.post("/pedido/remover-item/{id_item_pedido}")
async def RemoverItem(id_item_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    item_pedido = session.query(ItensPedido).filter(ItensPedido.id==id_item_pedido).first()
    pedido = session.query(Pedido).filter(Pedido.id==item_pedido.pedido_id).first()
    if not item_pedido:
        raise HTTPException(status_code=401, detail="item pedido não existente")
    if not usuario.admin and usuario.id != pedido.usuario_id:
        raise HTTPException(status_code=400, detail="Você não esta autorizado a fazer essa alteração!")
    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        "Messagem": "item pedido removido com sucesso",
        "preço pedido": pedido.preco,
        "Pedido": pedido
    }

@order_routers.post("/pedido/finalizar/{id_pedido}")
async def finalizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado!")
    if not usuario.admin and usuario.id != pedido.usuario_id:
        raise HTTPException(status_code=401, detail="Você não esta autorizado a alterar esse pedido!")
    pedido.status = "FINALIZADO"
    session.commit()
    return {
        "Menssagem": f"pedido {pedido.id} finalizado com sucesso",
        "Pedido": pedido
    }

@order_routers.get("/pedido/{id_pedido}")
async def visualizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado!")
    if not usuario.admin and usuario.id != pedido.usuario_id:
        raise HTTPException(status_code=401, detail="Você não esta autorizado a alterar esse pedido!")
    return {
        "Quantidade_itens_pedido": len(pedido.itens),
        "Pedido": pedido
    }


@order_routers.get("/list/pedido-usuario", response_model=List[ResponseSchemaPedidos])
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==usuario.id).all()
    return pedido