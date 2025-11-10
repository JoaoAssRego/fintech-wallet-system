from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, Async
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator
from app.config import settings

# Engine: Gerencia conexões com o banco
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,  # Log de queries SQL (útil pra debug!)
    future=True,
    pool_pre_ping=True,   # Verifica conexão antes de usar
    pool_size=10,         # Máximo de 10 conexões simultâneas
    max_overflow=20       # Pode criar até 20 extras se necessário
)

# Session Factory: Cria sessões (transações) com o banco
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Não expira objetos após commit
    autocommit=False,         # Controle manual de commit
    autoflush=False           # Controle manual de flush
)

# Base: Classe mãe de todos os models
Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:

    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)