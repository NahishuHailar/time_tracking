import pytest
from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repositories.project import ProjectRepository
from app.db.models.project import ProjectORM
from app.schemas.project import ProjectCreateSchema, ProjectUpdateSchema

@pytest.fixture
def mock_db_session():
    return AsyncMock(spec=AsyncSession)

@pytest.fixture
def project_repo(mock_db_session):
    return ProjectRepository(db=mock_db_session)

@pytest.mark.asyncio
async def test_get_by_id(project_repo, mock_db_session):
    mock_project = ProjectORM(id=1, name="Test Project")
    mock_db_session.get.return_value = mock_project

    project = await project_repo.get_by_id(1)
    
    assert project.id == 1
    assert project.name == "Test Project"
    mock_db_session.get.assert_called_once_with(ProjectORM, 1)

@pytest.mark.asyncio
async def test_create_project(project_repo, mock_db_session):
    project_data = ProjectCreateSchema(name="New Project")
    mock_project = ProjectORM(id=2, name=project_data.name)

    mock_db_session.add.return_value = None
    mock_db_session.flush.return_value = None
    mock_db_session.refresh.return_value = None

    project = await project_repo.create(project_data)

    assert project.name == "New Project"
    mock_db_session.add.assert_called_once()
    mock_db_session.flush.assert_called_once()
    mock_db_session.refresh.assert_called_once()

@pytest.mark.asyncio
async def test_update_project(project_repo, mock_db_session):
    mock_project = ProjectORM(id=3, name="Old Name")
    mock_db_session.get.return_value = mock_project

    update_data = ProjectUpdateSchema(name="Updated Name")
    project = await project_repo.update(3, update_data)

    assert project.name == "Updated Name"
    mock_db_session.flush.assert_called_once()
    mock_db_session.refresh.assert_called_once()

@pytest.mark.asyncio
async def test_delete_project(project_repo, mock_db_session):
    mock_project = ProjectORM(id=4, name="To Delete")
    mock_db_session.get.return_value = mock_project

    await project_repo.delete(4)

    mock_db_session.delete.assert_called_once_with(mock_project)
    mock_db_session.flush.assert_called_once()
