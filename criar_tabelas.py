import asyncio
from app.services.database import engine, Base

async def criar_tabelas():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)   # Opcional: limpa o banco antes
        await conn.run_sync(Base.metadata.create_all) # Cria as tabelas
    print("✅ Tabelas criadas com sucesso.")

if __name__ == "__main__":
    asyncio.run(criar_tabelas())
