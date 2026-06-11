from fastapi import APIRouter
# criar o router para as rotas de pedidos
order_routers = APIRouter(prefix="/orders", tags=["orders"])
# criar as rotas de pedidos
@order_routers.get("/")
async def pedidos():
    return {"message": "Lista de pedidos"}