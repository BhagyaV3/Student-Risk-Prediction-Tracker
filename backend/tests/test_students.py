from fastapi.testclient import TestClient


def create_user_and_get_token(client: TestClient):
    register_data = {
        "username": "student_teacher",
        "email": "student_teacher@example.com",
        "password": "secretpassword"
    }
    response = client.post("/api/auth/register", json=register_data)
    assert response.status_code == 201

    login_data = {
        "username": "student_teacher",
        "password": "secretpassword"
    }
    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200
    return response.json()["access_token"]


def test_student_crud_and_metrics(client: TestClient):
    token = create_user_and_get_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    student_payload = {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice@example.com"
    }
    response = client.post("/api/students", json=student_payload, headers=headers)
    assert response.status_code == 201
    student = response.json()
    assert student["first_name"] == "Alice"
    assert student["teacher_id"] == 1

    student_id = student["id"]

    response = client.get("/api/students", headers=headers)
    assert response.status_code == 200
    students = response.json()
    assert len(students) == 1
    assert students[0]["email"] == "alice@example.com"

    update_payload = {"last_name": "Jones"}
    response = client.put(f"/api/students/{student_id}", json=update_payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["last_name"] == "Jones"

    metrics_payload = {
        "attendance_percentage": 90.0,
        "gpa": 3.5,
        "assignment_completion_percentage": 88.0,
        "test_score_average": 85.0,
        "behavior_score": 92.0
    }
    response = client.post(f"/api/students/{student_id}/metrics", json=metrics_payload, headers=headers)
    assert response.status_code == 201
    metrics = response.json()
    assert metrics["student_id"] == student_id
    assert metrics["gpa"] == 3.5

    response = client.get(f"/api/students/{student_id}", headers=headers)
    assert response.status_code == 200
    student_detail = response.json()
    assert len(student_detail["metrics"]) == 1
    assert student_detail["metrics"][0]["gpa"] == 3.5

    response = client.delete(f"/api/students/{student_id}", headers=headers)
    assert response.status_code == 204

    response = client.get(f"/api/students/{student_id}", headers=headers)
    assert response.status_code == 404

def test_authorization_prevents_cross_teacher_access(client: TestClient):
    # Register teacher A and create a student
    client.post("/api/auth/register", json={
        "username": "teacher_a",
        "email": "teacher_a@example.com",
        "password": "passwordA"
    })
    login_a = client.post("/api/auth/login", json={
        "username": "teacher_a",
        "password": "passwordA"
    })
    headers_a = {"Authorization": f"Bearer {login_a.json()['access_token']}"}

    response = client.post("/api/students", json={
        "first_name": "Bob",
        "last_name": "Brown",
        "email": "bob@example.com"
    }, headers=headers_a)
    assert response.status_code == 201
    student_id = response.json()["id"]

    # Register teacher B
    client.post("/api/auth/register", json={
        "username": "teacher_b",
        "email": "teacher_b@example.com",
        "password": "passwordB"
    })
    login_b = client.post("/api/auth/login", json={
        "username": "teacher_b",
        "password": "passwordB"
    })
    headers_b = {"Authorization": f"Bearer {login_b.json()['access_token']}"}

    # Teacher B tries to access teacher A's student → should get 403
    response = client.get(f"/api/students/{student_id}", headers=headers_b)
    assert response.status_code == 403

    # Teacher B tries to delete teacher A's student → should get 403
    response = client.delete(f"/api/students/{student_id}", headers=headers_b)
    assert response.status_code == 403
