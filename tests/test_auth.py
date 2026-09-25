async def test_register_user(client):
    response = await client.post("/users", json={
        "email": "u1@example.com",
        "name": "User One",
        "password": "password123",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "u1@example.com"
    assert "hashed_password" not in data


async def test_login_success(client):
    await client.post("/users", json={
        "email": "u2@example.com",
        "name": "User Two",
        "password": "password123",
    })
    response = await client.post("/auth/login", data={
        "username": "u2@example.com",
        "password": "password123",
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


async def test_login_wrong_password(client):
    await client.post("/users", json={
        "email": "u3@example.com",
        "name": "User Three",
        "password": "password123",
    })
    response = await client.post("/auth/login", data={
        "username": "u3@example.com",
        "password": "wrong",
    })
    assert response.status_code == 401


async def test_me_without_token(client):
    response = await client.get("/auth/me")
    assert response.status_code == 401


async def test_me_with_token(client):
    await client.post("/users", json={
        "email": "u4@example.com",
        "name": "User Four",
        "password": "password123",
    })
    login = await client.post("/auth/login", data={
        "username": "u4@example.com",
        "password": "password123",
    })
    token = login.json()["access_token"]

    response = await client.get(
        "/auth/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "u4@example.com"