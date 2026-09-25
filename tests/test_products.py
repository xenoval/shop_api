async def test_create_product(client):
    response = await client.post("/products", json={
        "name": "IPhone 18 pro",
        "description": "Цвет: черный, Объем памяти: 1 Тб, Тип SIM-карт: eSIM",
        "price": "239990.00",
    })

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "IPhone 18 pro"
    assert data["description"] == "Цвет: черный, Объем памяти: 1 Тб, Тип SIM-карт: eSIM"
    assert "id" in data


async def test_list_products(client):
    for i in range(2):
        await client.post("/products", json={
            "name": f"Product {i}",
            "description": "desc",
            "price": "10.00",
        })

    response = await client.get("/products")
    assert response.status_code == 200
    body = response.json()
    assert len(body["items"]) >= 2


async def test_get_product_by_id(client):
    created = await client.post("/products", json={
        "name": "Find Me",
        "description": "desc",
        "price": "100.00",
    })
    product_id = created.json()["id"]

    response = await client.get(f"/products/{product_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == "Find Me"


async def test_get_product_not_found(client):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = await client.get(f"/products/{fake_id}")
    assert response.status_code == 404


async def test_pagination(client):
    for i in range(3):
        await client.post("/products", json={
            "name": f"Paged {i}",
            "description": "d",
            "price": "10.00",
        })

    response = await client.get("/products", params={"limit": 2, "offset": 0})
    assert response.status_code == 200
    body = response.json()
    assert "items" in body
    assert len(body["items"]) == 2
    assert body["limit"] == 2
    assert body["offset"] == 0

    response2 = await client.get("/products", params={"limit": 2, "offset": 1})
    assert response2.status_code == 200
    body2 = response2.json()
    assert len(body2["items"]) == 1
    assert body2["total"] == 3

    first_ids = {p["id"] for p in body["items"]}
    second_ids = {p["id"] for p in body2["items"]}
    assert first_ids.isdisjoint(second_ids)