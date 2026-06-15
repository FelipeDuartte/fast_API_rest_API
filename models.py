from sqlalchemy import create_engine, String, Integer, Boolean, Float, Column, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType
# criar a conexao com o banco de dados
db = create_engine("sqlite:///banco.db")
# criar a base de dados
Base = declarative_base()
# criar a classe/tabela de pedidos

class Usuario(Base):
    # nome da tabela
    __tablename__ = "usuarios"
    # valores padrao que tem que ter na tabela de usuarios
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String, nullable=False)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default=False)
    # oque tenho que passar para criar um usuario
    def __init__(self, nome, email, senha, ativo=False, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin


class Pedido(Base):
    # nome da tabela
    __tablename__ = "pedidos"
    # valores padrao que tem que ter na tabela de pedidos
    # STATUS_PEDIDO = [
    #     ("PENDENTE", "PENDENTE"),
    #     ("CANCELADO", "CANCELADO"),
    #     ("CONCLUIDO", "CONCLUIDO")
    # ]

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String)
    preco = Column("preco", Float)
    usuario_id = Column("usuario_id", Integer, ForeignKey("usuarios.id"))
    # oque tenho que passar para criar um pedido
    def __init__(self, usuario_id, status="PENDENTE", preco=0.0):
        self.status = status
        self.preco = preco
        self.usuario_id = usuario_id

class ItensPedido(Base):
    __tablename__ = "itens_pedido"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade = Column("quantidade", Integer)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido_id = Column("pedido_id", Integer, ForeignKey("pedidos.id"))

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido_id):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido_id = pedido_id
