import os

# Gerar os arquivos para o CRUD de hospitais e primeiro usuário
hospital_crud_files = {
    "app/models/hospital.py": """\
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from app.models.usuario import Usuario
from app.services.database import Base

class Hospital(Base):
    __tablename__ = "hospital"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    turnos = Column(Integer, nullable=False)
    funcoes = Column(ARRAY(String), nullable=False)

    usuarios = relationship("Usuario", back_populates="hospital")
""",

    "app/models/usuario.py": """\
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.services.database import Base

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    permissao = Column(String, nullable=False)

    hospital_id = Column(Integer, ForeignKey("hospital.id"))
    hospital = relationship("Hospital", back_populates="usuarios")
""",

    "app/services/database.py": """\
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

Base = declarative_base()
engine = create_async_engine(settings.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with SessionLocal() as session:
        yield session
""",

    "app/schemas/hospital.py": """\
from typing import List
from pydantic import BaseModel

class HospitalCreate(BaseModel):
    nome: str
    turnos: int
    funcoes: List[str]
    admin_nome: str
    admin_email: str
    admin_senha: str

class HospitalOut(BaseModel):
    id: int
    nome: str
    turnos: int
    funcoes: List[str]

    class Config:
        orm_mode = True
""",

    "app/routes/hospital.py": """\
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext

from app.models.hospital import Hospital
from app.models.usuario import Usuario
from app.schemas.hospital import HospitalCreate, HospitalOut
from app.services.database import get_db

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/hospitais", response_model=HospitalOut)
async def criar_hospital(dados: HospitalCreate, db: AsyncSession = Depends(get_db)):
    novo_hospital = Hospital(
        nome=dados.nome,
        turnos=dados.turnos,
        funcoes=dados.funcoes
    )
    db.add(novo_hospital)
    await db.flush()  # para pegar novo_hospital.id

    hash_senha = pwd_context.hash(dados.admin_senha)
    usuario_admin = Usuario(
        nome=dados.admin_nome,
        email=dados.admin_email,
        senha_hash=hash_senha,
        permissao="admin",
        hospital_id=novo_hospital.id
    )
    db.add(usuario_admin)
    await db.commit()
    await db.refresh(novo_hospital)
    return novo_hospital
""",

    "app/main.py": """\
from fastapi import FastAPI
from app.routes import hospital
from app.core.config import settings

app = FastAPI(title="Dose Certa")

app.include_router(hospital.router)

@app.get("/")
def root():
    return {"message": "API Dose Certa rodando!"}
"""
}

# Criar os arquivos dentro da estrutura atual
base_path = "C:/Users/rbarr/Dose_certa"
for rel_path, content in hospital_crud_files.items():
    full_path = os.path.join(base_path, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

"Arquivos para CRUD de hospital e criação do primeiro usuário admin foram gerados com sucesso."
