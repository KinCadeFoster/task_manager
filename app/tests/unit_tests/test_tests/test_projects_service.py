import pytest

from app.projects.service import ProjectService


@pytest.mark.parametrize("name, prefix_name, description, creator_id",[
    ("Project 1", "PRA", "Project 1 description", 2),
])

async def test_add_project(name, prefix_name, description, creator_id):
    project = await ProjectService.add(name=name, prefix_name=prefix_name, description=description, creator_id=creator_id)

    assert project.name == name
    assert project.prefix_name == prefix_name
    assert project.description == description
    assert project.creator_id == creator_id

@pytest.mark.parametrize("project_id, updated_name, updated_description",[
    (1, "Updated project 1", "Updated project 1 description"),
])

async def test_update_project(project_id, updated_name, updated_description):
    project = await ProjectService.update_by_id(object_id=project_id, name=updated_name, description=updated_description)

    assert project.name == updated_name
    assert project.description == updated_description

@pytest.mark.parametrize("project_id, updated_name",[
    (1, "Updated project 1"),
])

async def test_update_name_project(project_id, updated_name):
    project = await ProjectService.update_by_id(object_id=project_id, name=updated_name)

    assert project.name == updated_name

@pytest.mark.parametrize("project_id, updated_description",[
    (1, "Updated project 1 description"),
])

async def test_update_description_project(project_id, updated_description):
    project = await ProjectService.update_by_id(object_id=project_id, description=updated_description)

    assert project.description == updated_description

async def test_delete_project():
    project = await ProjectService.delete_by_id(object_id=1)
    assert project == True

    delete_project = await ProjectService.find_by_id(1)
    assert delete_project is None

async def test_find_all_project():
    projects = await ProjectService.find_all()

    assert len(projects) == 2

async def test_none_project():
    await ProjectService.delete_by_id(object_id=2)
    await ProjectService.delete_by_id(object_id=3)
    projects = await ProjectService.find_all()


    for project in projects: print(project)
    assert projects == []


async def test_update_nonexistent_project():
    result = await ProjectService.update_by_id(object_id=9999, name="new name", description="new desc")
    assert result is None


async def test_delete_project_twice():
    project = await ProjectService.add(
        name="To delete twice",
        prefix_name="DEL2X",
        description="Delete me twice",
        creator_id=2
    )

    result_first = await ProjectService.delete_by_id(project.id)
    assert result_first is True

    result_second = await ProjectService.delete_by_id(project.id)
    assert result_second is False