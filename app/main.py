from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from contextlib import asynccontextmanager

from app.config import settings
from app.database import get_db, init_db, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia startup e shutdown"""
    # STARTUP
    await init_db()
 
    yield  # App rodando aqui
    
    # SHUTDOWN
    await engine.dispose()

# Criar aplicação FastAPI
app = FastAPI(
    title=settings.app_name,
    description="Sistema de Carteira Digital com FastAPI, PostgreSQL e JWT",
    version="1.0.0",
    lifespan=lifespan    
)

@app.get("/")
async def root():
    """
    Endpoint raiz - Boas-vindas
    """
    return {
        "message": "🏦 Digital Wallet API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """
    Health check - Verifica se API e banco estão funcionando
    
    Testa:
    - API respondendo
    - Conexão com banco funcionando
    """
    try:
        # Tenta fazer uma query simples no banco
        result = await db.execute(text("SELECT 1"))
        result.scalar()
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "healthy",
                "api": "✅ online",
                "database": "✅ connected"
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "api": "✅ online",
                "database": f"❌ error: {str(e)}"
            }
        )