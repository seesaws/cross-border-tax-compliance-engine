"""FastAPI REST API 测试"""

from fastapi.testclient import TestClient

from interface.api.app import app

client = TestClient(app)


class TestAPI:
    def test_health(self):
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

    def test_list_countries(self):
        r = client.get("/api/countries")
        assert r.status_code == 200
        codes = [c["code"] for c in r.json()["countries"]]
        assert "UK" in codes
        assert "US" in codes

    def test_get_rates_uk(self):
        r = client.get("/api/rates/UK")
        assert r.status_code == 200
        data = r.json()
        assert data["country"] == "UK"
        assert data["rates"]["standard"]["rate"] == "0.20"

    def test_get_rates_invalid(self):
        r = client.get("/api/rates/ZZ")
        assert r.status_code == 404

    def test_calculate_uk(self):
        r = client.post("/api/calculate", json={
            "country": "UK",
            "items": [{"name": "耳机", "quantity": 1, "unit_price": "100"}],
        })
        assert r.status_code == 200
        data = r.json()
        assert data["total_tax"] == "20.00"
        assert data["total_with_tax"] == "120.00"

    def test_calculate_us_texas(self):
        r = client.post("/api/calculate", json={
            "country": "US",
            "state": "TX",
            "items": [{"name": "书包", "quantity": 2, "unit_price": "50"}],
        })
        assert r.status_code == 200
        assert r.json()["total_tax"] == "6.25"

    def test_batch(self):
        r = client.post("/api/batch", json=[
            {"order_id": "B-1", "country": "UK", "items": [{"name": "A", "quantity": 1, "unit_price": "100"}]},
            {"order_id": "B-2", "country": "DE", "items": [{"name": "B", "quantity": 1, "unit_price": "100"}]},
        ])
        assert r.status_code == 200
        assert len(r.json()) == 2
