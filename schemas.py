from pydantic import BaseModel
from typing import Optional

class SchemaUsuario(BaseModel):

    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_attributes= True

class SchemaPedido(BaseModel):

    usuario_id: int

    class Config:
        from_attributes= True

class SchemaLogin(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes= True

class SchemaItemPedido(BaseModel):
    quantidade: int
    sabor: str
    tamanho: str
    preco_unitario: float
    pedido_id: int