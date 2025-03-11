import pytest

from app.db.models.project import ProjectORM


@pytest.mark.asyncio
async def test_create_project(client, test_db):
    response = await client.post("/api/v1/projects/", json={"name": "New Project"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Project"
    assert "id" in data

@pytest.mark.asyncio
async def test_get_project(client, test_db):
    project = ProjectORM(name="Test Project")
    test_db.add(project)
    await test_db.flush()
    await test_db.refresh(project)

    response = await client.get(f"/api/v1/projects/{project.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == project.id
    assert data["name"] == project.name

@pytest.mark.asyncio
async def test_update_project(client, test_db):
    project = ProjectORM(name="Old Name")
    test_db.add(project)
    await test_db.flush()
    await test_db.refresh(project)

    response = await client.put(f"/api/v1/projects/{project.id}", json={"name": "Updated Name"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"

@pytest.mark.asyncio
async def test_delete_project(client, test_db):
    project = ProjectORM(name="To Delete")
    test_db.add(project)
    await test_db.flush()
    await test_db.refresh(project)

    response = await client.delete(f"/api/v1/projects/{project.id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Project deleted"}

    response = await client.get(f"/api/v1/projects/{project.id}")
    assert response.status_code == 404
