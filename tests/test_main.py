def test_health_check(client):
    """Testar endpoint de health check"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "nuvie-backend"
    assert data["version"] == "2.0.0"

def test_root_endpoint(client):
    """Testar endpoint raiz"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
