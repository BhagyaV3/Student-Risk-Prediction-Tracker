from unittest.mock import patch
from fastapi.testclient import TestClient

MOCK_PREDICTION = {
    "prediction_label": "high",
    "prediction_score": 0.82,
    "confidence": 0.91,
    "feature_importance": {
        "attendance_percentage": 0.42,
        "gpa": 0.31,
        "assignment_completion_percentage": 0.12,
        "test_score_average": 0.09,
        "behavior_score": 0.06,
    },
}


def create_user_and_get_token(client: TestClient, username: str, email: str):
    client.post("/api/auth/register", json={
        "username": username,
        "email": email,
        "password": "testpassword"
    })
    response = client.post("/api/auth/login", json={
        "username": username,
        "password": "testpassword"
    })
    return response.json()["access_token"]


def create_student(client: TestClient, headers: dict):
    response = client.post("/api/students", json={
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com"
    }, headers=headers)
    return response.json()["id"]


def add_metrics(client: TestClient, student_id: int, headers: dict):
    client.post(f"/api/students/{student_id}/metrics", json={
        "attendance_percentage": 45.0,
        "gpa": 1.2,
        "assignment_completion_percentage": 40.0,
        "test_score_average": 38.0,
        "behavior_score": 35.0,
    }, headers=headers)


@patch("app.routes.predictions.ml_service.predict", return_value=MOCK_PREDICTION)
def test_predict_success(mock_predict, client: TestClient):
    token = create_user_and_get_token(client, "teacher1", "t1@example.com")
    headers = {"Authorization": f"Bearer {token}"}
    student_id = create_student(client, headers)
    add_metrics(client, student_id, headers)

    response = client.post("/api/predictions/predict",
                           json={"student_id": student_id},
                           headers=headers)

    assert response.status_code == 201
    data = response.json()
    assert data["prediction_label"] == "high"
    assert data["prediction_score"] == 0.82
    assert data["confidence"] == 0.91
    assert "attendance_percentage" in data["feature_importance"]
    assert data["student_id"] == student_id
    mock_predict.assert_called_once()


@patch("app.routes.predictions.ml_service.predict", return_value=MOCK_PREDICTION)
def test_predict_no_metrics(mock_predict, client: TestClient):
    token = create_user_and_get_token(client, "teacher2", "t2@example.com")
    headers = {"Authorization": f"Bearer {token}"}
    student_id = create_student(client, headers)

    response = client.post("/api/predictions/predict",
                           json={"student_id": student_id},
                           headers=headers)

    assert response.status_code == 404
    assert "No metrics" in response.json()["detail"]


@patch("app.routes.predictions.ml_service.predict", return_value=MOCK_PREDICTION)
def test_predict_wrong_teacher(mock_predict, client: TestClient):
    token_a = create_user_and_get_token(client, "teacher3", "t3@example.com")
    headers_a = {"Authorization": f"Bearer {token_a}"}
    student_id = create_student(client, headers_a)

    token_b = create_user_and_get_token(client, "teacher4", "t4@example.com")
    headers_b = {"Authorization": f"Bearer {token_b}"}

    response = client.post("/api/predictions/predict",
                           json={"student_id": student_id},
                           headers=headers_b)

    assert response.status_code == 403


@patch("app.routes.predictions.ml_service.predict", return_value=MOCK_PREDICTION)
def test_list_predictions(mock_predict, client: TestClient):
    token = create_user_and_get_token(client, "teacher5", "t5@example.com")
    headers = {"Authorization": f"Bearer {token}"}
    student_id = create_student(client, headers)
    add_metrics(client, student_id, headers)

    client.post("/api/predictions/predict",
                json={"student_id": student_id},
                headers=headers)
    client.post("/api/predictions/predict",
                json={"student_id": student_id},
                headers=headers)

    response = client.get(f"/api/students/{student_id}/predictions", headers=headers)

    assert response.status_code == 200
    assert len(response.json()) == 2


@patch("app.routes.predictions.ml_service.predict", return_value=MOCK_PREDICTION)
def test_get_latest_prediction(mock_predict, client: TestClient):
    token = create_user_and_get_token(client, "teacher6", "t6@example.com")
    headers = {"Authorization": f"Bearer {token}"}
    student_id = create_student(client, headers)
    add_metrics(client, student_id, headers)

    client.post("/api/predictions/predict",
                json={"student_id": student_id},
                headers=headers)

    response = client.get(f"/api/students/{student_id}/predictions/latest", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["prediction_label"] == "high"
    assert data["student_id"] == student_id


def test_get_latest_prediction_none_exist(client: TestClient):
    token = create_user_and_get_token(client, "teacher7", "t7@example.com")
    headers = {"Authorization": f"Bearer {token}"}
    student_id = create_student(client, headers)

    response = client.get(f"/api/students/{student_id}/predictions/latest", headers=headers)

    assert response.status_code == 404