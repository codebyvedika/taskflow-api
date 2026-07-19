def test_create_task(client, sample_project):
    response = client.post(
        f"/api/v1/projects/{sample_project['id']}/tasks",
        json={"title": "Set up CI pipeline", "priority": "urgent"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "todo"
    assert data["priority"] == "urgent"


def test_create_task_for_nonexistent_project_404(client):
    response = client.post(
        "/api/v1/projects/00000000-0000-0000-0000-000000000000/tasks",
        json={"title": "Ghost task"},
    )
    assert response.status_code == 404


def test_list_tasks_with_filters(client, sample_project, sample_task):
    client.post(
        f"/api/v1/projects/{sample_project['id']}/tasks",
        json={"title": "Low priority cleanup", "priority": "low"},
    )

    high_priority = client.get(f"/api/v1/projects/{sample_project['id']}/tasks?priority_filter=high")
    assert len(high_priority.json()) == 1

    all_tasks = client.get(f"/api/v1/projects/{sample_project['id']}/tasks")
    assert len(all_tasks.json()) == 2


def test_update_task_status_flow(client, sample_task):
    response = client.patch(f"/api/v1/tasks/{sample_task['id']}/status", json={"status": "in_progress"})
    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"


def test_project_stats_reflect_done_tasks(client, sample_project, sample_task):
    client.patch(f"/api/v1/tasks/{sample_task['id']}/status", json={"status": "done"})

    response = client.get(f"/api/v1/projects/{sample_project['id']}")
    data = response.json()
    assert data["total_tasks"] == 1
    assert data["done_tasks"] == 1


def test_add_comment_to_task(client, sample_task):
    response = client.post(
        f"/api/v1/tasks/{sample_task['id']}/comments",
        json={"author_name": "Amit", "content": "Looks good, one small fix needed on mobile view."},
    )
    assert response.status_code == 201
    assert response.json()["author_name"] == "Amit"


def test_list_comments_for_task(client, sample_task):
    client.post(
        f"/api/v1/tasks/{sample_task['id']}/comments",
        json={"author_name": "Amit", "content": "First comment"},
    )
    client.post(
        f"/api/v1/tasks/{sample_task['id']}/comments",
        json={"author_name": "Riya", "content": "Second comment"},
    )

    response = client.get(f"/api/v1/tasks/{sample_task['id']}/comments")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_activity_log_records_task_lifecycle(client, sample_task):
    client.patch(f"/api/v1/tasks/{sample_task['id']}/status", json={"status": "in_progress"})
    client.post(
        f"/api/v1/tasks/{sample_task['id']}/comments",
        json={"author_name": "Amit", "content": "Started working on this"},
    )

    response = client.get(f"/api/v1/tasks/{sample_task['id']}/activity")
    assert response.status_code == 200
    actions = [entry["action"] for entry in response.json()]

    assert "TASK_CREATED" in actions
    assert "STATUS_CHANGED" in actions
    assert "COMMENT_ADDED" in actions


def test_delete_task_removes_it(client, sample_task):
    response = client.delete(f"/api/v1/tasks/{sample_task['id']}")
    assert response.status_code == 204

    check = client.get(f"/api/v1/tasks/{sample_task['id']}")
    assert check.status_code == 404