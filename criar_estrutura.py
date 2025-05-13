import os

project_structure = {
    "dose_certa": {
        "app": {
            "models": {},
            "routes": {},
            "schemas": {},
            "services": {},
            "core": {
                "config.py": """\
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
"""
            },
            "main.py": """\
from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(title="Dose Certa")

@app.get("/")
def root():
    return {"message": "API Dose Certa rodando!"}
"""
        },
        ".env": """\
DATABASE_URL=postgresql+asyncpg://postgres:senha@localhost:5432/dosecerta
SECRET_KEY=chave-super-secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
""",
        "requirements.txt": """\
fastapi
uvicorn
sqlalchemy
asyncpg
python-dotenv
alembic
passlib[bcrypt]
python-jose[cryptography]
pydantic
"""
    }
}

def create_project_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_project_structure(path, content)
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

# ALTERE AQUI SE QUISER CRIAR EM OUTRO LUGAR:
base_path = os.getcwd()
create_project_structure(base_path, project_structure["dose_certa"])

print("✅ Projeto criado com sucesso em:", os.path.join(base_path, "dose_certa"))
