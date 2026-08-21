from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200

    delete_response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == f"Unregistered {email} from {activity_name}"

    activity_response = client.get("/activities")
    assert email not in activity_response.json()[activity_name]["participants"]


def test_unregister_unknown_participant_returns_404():
    response = client.delete("/activities/Chess Club/unregister?email=ghost@mergington.edu")
    assert response.status_code == 404
