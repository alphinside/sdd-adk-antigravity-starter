import os
import sys

# Garante que o diretório raiz do repositório esteja no sys.path
sys.path.insert(0, os.path.abspath("."))

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from httpx import AsyncClient, ASGITransport

# Configura as variáveis de ambiente para os testes
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["RESERVATIONS_API_KEY"] = "secret123"

# Importações atrasadas para permitir que as variáveis de ambiente tenham efeito
from restaurant_concierge.database import Base, get_db
from server import app

test_engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    echo=False,
    future=True,
)

TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(autouse=True)
async def setup_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
