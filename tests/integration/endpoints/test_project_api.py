import pytest
from httpx import AsyncClient
from app.main import app
from app.db.session import database
from app.db.models.project import ProjectORM

@pytest.fixture
async def test_db():
    async with database.async_session() as session:
        yield session  
        await session.rollback()  

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac  

@pytest.mark.asyncio
async def test_create_project(client, test_db):
    response = await client.post("/api/v1/projects/", json={"name": "New Project"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Project"
    assert "id" in data

@pytest.mark.asyncio
async def test_get_project(client, test_db):
    project = ProjectORM(id=1, name="Test Project")
    test_db.add(project)
    await test_db.flush()

    response = await client.get(f"/api/v1/projects/{project.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == project.id
    assert data["name"] == project.name

@pytest.mark.asyncio
async def test_update_project(client, test_db):
    project = ProjectORM(id=2, name="Old Name")
    test_db.add(project)
    await test_db.flush()

    response = await client.put(f"/api/v1/projects/{project.id}", json={"name": "Updated Name"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"

@pytest.mark.asyncio
async def test_delete_project(client, test_db):
    project = ProjectORM(id=3, name="To Delete")
    test_db.add(project)
    await test_db.flush()

    response = await client.delete(f"/api/v1/projects/{project.id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Project deleted"}

    response = await client.get(f"/api/v1/projects/{project.id}")
    assert response.status_code == 404  
