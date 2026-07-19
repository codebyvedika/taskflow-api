def test_create_project(client):
    response = client.post("/api/v1/projects", json={"name": "Mobile App Launch"})
    assert response.status_code == 201
    assert response.json()["name"] == "Mobile App Launch"


def test_create_project_invalid_fails(client):
    response = client.post("/api/v1/projects", json={"name": "A"})
    assert response.status_code == 422


def test_list_projects(client, sample_project):
    response = client.get("/api/v1/projects")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_project_with_stats(client, sample_project):
    response = client.get(f"/api/v1/projects/{sample_project['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["total_tasks"] == 0
    assert data["done_tasks"] == 0


def test_get_nonexistent_project_404(client):
    response = client.get("/api/v1/projects/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_update_project(client, sample_project):
    response = client.patch(f"/api/v1/projects/{sample_project['id']}", json={"name": "Renamed Project"})
    assert response.status_code == 200
    assert response.json()["name"] == "Renamed Project"


def test_delete_project_cascades_tasks(client, sample_project, sample_task):
    response = client.delete(f"/api/v1/projects/{sample_project['id']}")
    assert response.status_code == 204

    check_task = client.get(f"/api/v1/tasks/{sample_task['id']}")
    assert check_task.status_code == 404