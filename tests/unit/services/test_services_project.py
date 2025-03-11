from unittest.mock import AsyncMock

import pytest

from app.db.models.project import ProjectORM
from app.db.repositories.project import ProjectRepository
from app.schemas.project import ProjectCreateSchema, ProjectUpdateSchema
from app.services.project import ProjectService


@pytest.fixture
def mock_project_repo():
    return AsyncMock(spec=ProjectRepository)

@pytest.fixture
def project_service(mock_project_repo):
    return ProjectService(project_repository=mock_project_repo)

@pytest.mark.asyncio
async def test_get_project(project_service, mock_project_repo):
    mock_project = ProjectORM(id=1, name="Test Project")
    mock_project_repo.get_by_id.return_value = mock_project

    project = await project_service.get_project(1)

    assert project.id == 1
    assert project.name == "Test Project"
    mock_project_repo.get_by_id.assert_called_once_with(1)

@pytest.mark.asyncio
async def test_create_project(project_service, mock_project_repo):
    project_data = ProjectCreateSchema(name="New Project")
    mock_project = ProjectORM(id=2, name=project_data.name)
    mock_project_repo.create.return_value = mock_project

    project = await project_service.create_project(project_data)

    assert project.id == 2
    assert project.name == "New Project"
    mock_project_repo.create.assert_called_once_with(project_data)

@pytest.mark.asyncio
async def test_update_project(project_service, mock_project_repo):
    mock_project = ProjectORM(id=3, name="Old Name")

    async def mock_update(_id, data):
        mock_project.name = data.name
        return mock_project

    mock_project_repo.update.side_effect = mock_update

    update_data = ProjectUpdateSchema(name="Updated Name")
    project = await project_service.update_project(3, update_data)

    assert project.name == "Updated Name"
    mock_project_repo.update.assert_called_once_with(3, update_data)

@pytest.mark.asyncio
async def test_delete_project(project_service, mock_project_repo):
    await project_service.delete_project(4)

    mock_project_repo.delete.assert_called_once_with(4)
