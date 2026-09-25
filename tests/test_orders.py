# POST /orders с существующим товаром → успех, 
# проверь order_id и total.

# POST /orders с несуществующим товаром → 400 
# (или та ошибка, которую ты кидаешь в сервисе).

async def test_create_order(client):
    created = await client.post("/products", json={
            "name": "Find Me",
            "description": "desc",
            "price": "100.00",
        })
    product_id = created.json()["id"]

    created = await client.post("/users", json={
        "email": "u1@example.com",
        "name": "User One",
        "password": "password123",
    })
    user_id = created.json()["id"]

    response = await client.post("/orders", json={
        "user_id": user_id,
        "items": [
            {
            "product_id": product_id,
            "quantity": 2
            },
        ],
    })

    assert response.status_code == 200
    data = response.json()
    assert "order_id" in data
    assert data["total"] == 200.0


async def test_create_order_wrong_id(client):
    created = await client.post("/users", json={
        "email": "u1@example.com",
        "name": "User One",
        "password": "password123",
    })
    user_id = created.json()["id"]

    fake_product_id = "00000000-0000-0000-0000-000000000000"

    response = await client.post("/orders", json={
        "user_id": user_id,
        "items": [
            {
            "product_id": fake_product_id,
            "quantity": 2
            },
        ],
    })

    assert response.status_code == 404