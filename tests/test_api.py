from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to the Kenya Climate Data Lab API" in response.json()["message"]

def test_get_counties():
    response = client.get("/counties")
    assert response.status_code == 200
    assert response.json()["count"] == 47
    assert "Nakuru" in response.json()["counties"]

def test_get_valid_county_stress():
    response = client.get("/stress/Nakuru")
    assert response.status_code == 200
    assert response.json()["county"] == "Nakuru"
    assert len(response.json()["data"]) > 0
    assert "stress_avg" in response.json()["data"][0]

def test_get_invalid_county():
    response = client.get("/stress/Atlantis")
    assert response.status_code == 404
    assert response.json()["detail"] == "County 'Atlantis' not found."
