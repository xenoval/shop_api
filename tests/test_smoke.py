async def test_client_works(client):
    response = await client.get("/docs")
    assert response.status_code == 200