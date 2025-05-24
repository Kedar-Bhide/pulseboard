from app.core.security import create_access_token

def test_get_current_user(client, test_user):
    access_token = create_access_token(data={"sub": test_user.email})
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user.email
    assert data["full_name"] == test_user.full_name

def test_get_current_user_unauthorized(client):
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_update_current_user(client, test_user):
    access_token = create_access_token(data={"sub": test_user.email})
    response = client.patch(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"full_name": "Updated Name"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Name"

def test_update_current_user_invalid_data(client, test_user):
    access_token = create_access_token(data={"sub": test_user.email})
    response = client.patch(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"email": "invalid-email"}
    )
    assert response.status_code == 422 