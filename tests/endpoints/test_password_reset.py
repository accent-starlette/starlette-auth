def test_get(client):
    response = client.get("/auth/password/reset")
    assert response.status_code == 200
    assert "form" in response.context
    assert "request" in response.context
