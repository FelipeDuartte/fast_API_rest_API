from fastapi import APIRouter, Depends, HTTPException
from models import Usuario, db
from dependencies import pegar_sessao
from main import bcrypt_context
from schemas import SchemaUsuario
auth_routers = APIRouter(prefix="/auth", tags=["auth"])

@auth_routers.get("/")
async def autenticacao():
    return {"message": "Rota de autenticação"}

@auth_routers.post("/criar_conta")
async def criar_conta(usuario_schema: SchemaUsuario, session=Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
    if usuario:
        # verifica se o email já existe
        raise HTTPException(status_code=400, detail="E-mail ja cadastrado!")
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin)
        session.add(novo_usuario)
        session.commit()
        return {"message": f"Usuário criado com sucesso {usuario_schema.email}"}