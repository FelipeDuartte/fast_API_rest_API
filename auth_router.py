from fastapi import APIRouter, Depends, HTTPException
from models import Usuario, db
from dependencies import pegar_sessao, verificar_token
from main import bcrypt_context, ACCESS_TOKEN_EXPIRE_MINUTE, ALGORITHM, SECRET_KEY
from schemas import SchemaUsuario, SchemaLogin
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth_routers = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(usuario_id, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)):
    data_expire = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": str(usuario_id), "exp": data_expire}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return jwt_codificado

def autenticar_usuario(email,senha,session):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario

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
    
@auth_routers.post("/login")
async def Login(login_schema: SchemaLogin, session: Session=Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario não encontrado ou credenciais invalidas!")
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, timedelta(days=7))
        return {
            "access_token": f"{access_token}",
            "refresh_token": f"{refresh_token}",
            "token_type": "Bearer"
        }
    
@auth_routers.post("/login-form")
async def Login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session=Depends(pegar_sessao)):
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario não encontrado ou credenciais invalidas!")
    else:
        access_token = criar_token(usuario.id)
        return {
            "access_token": f"{access_token}",
            "token_type": "Bearer"
        }    

@auth_routers.get("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    access_token = criar_token(usuario.id)
    return {
            "access_token": f"{access_token}",
            "token_type": "Bearer"
        }