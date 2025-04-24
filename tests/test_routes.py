import sys
import os
import asyncio
import pytest
import pytest_asyncio

# ajusta o PYTHONPATH para encontrar o app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from main import app
from app.core.config import get_settings
from app.core.database import Base, engine, get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

settings = get_settings()

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield

@pytest_asyncio.fixture()
async def db_session():
    AsyncSessionLocal = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with AsyncSessionLocal() as session:
        yield session

@pytest_asyncio.fixture()
async def async_client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://0.0.0.0"
    ) as client:
        yield client

# dados de exemplo
mock_user = {
    "email": "teste@teste.com",
    "password": "123456"
}

payload = {
    "name": "teste",
    "email": "teste@teste.com",
    "password": "123456",
    "role": "system"
}

@pytest.mark.asyncio
async def test_ping(async_client):
    
    response = await async_client.get(f"{settings.api_v1_str}/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "SGIO API Online"}

@pytest.mark.asyncio
async def test_register_user(async_client):

    r = await async_client.post(f"{settings.api_v1_str}/auth/register", json=payload)
    assert r.status_code == 200

@pytest.mark.asyncio
async def test_login(async_client):

    r1 = await async_client.post(f"{settings.api_v1_str}/auth/register", json=payload)
    assert r1.status_code == 200

    r2 = await async_client.post(f"{settings.api_v1_str}/auth/login", json=mock_user)
    assert r2.status_code == 200
    body = r2.json()
    assert "access_token" in body
    
@pytest.mark.asyncio
async def test_get_user_me(async_client):
    
    await async_client.post(
        f"{settings.api_v1_str}/auth/register", json=payload
    )
    
    token = (await async_client.post(f"{settings.api_v1_str}/auth/login", json=mock_user)).json()["access_token"]

    r = await async_client.get(
        f"{settings.api_v1_str}/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert r.status_code == 200
    assert r.json()["email"] == mock_user["email"]