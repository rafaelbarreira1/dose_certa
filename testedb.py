import asyncio
from app.services.database import engine

async def testar_conexao():
    async with engine.begin() as conn:
        result = await conn.execute("SELECT current_database(), inet_server_addr(), inet_client_addr();")
        print(result.fetchall())

if __name__ == "__main__":
    asyncio.run(testar_conexao())
