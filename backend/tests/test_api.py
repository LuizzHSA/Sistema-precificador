from datetime import datetime, timedelta
import pytest
from app.main import create_app
from app import db
from app.models import Store, Product


@pytest.fixture()
def client():
    app = create_app("testing")
    with app.app_context():
        db.drop_all()
        db.create_all()
    with app.test_client() as client:
        yield client
    with app.app_context():
        db.session.remove()
        db.drop_all()


def auth(client):
    response = client.post("/api/auth/login", json={"email": "admin@pricetracker.com", "password": "admin123"})
    return {"Authorization": f"Bearer {response.json['token']}"}


def catalog(client):
    headers = auth(client)
    store = client.post("/api/stores", headers=headers, json={"name": "Loja Teste", "email": "teste@example.com"}).json["data"]
    product = client.post("/api/products", headers=headers, json={"store_id": store["id"], "name": "Produto", "sku": "SKU-1", "current_price": 100}).json["data"]
    return headers, store, product


def test_health_and_auth(client):
    assert client.get("/health").status_code == 200
    assert client.get("/api/auth/me").status_code == 401
    assert client.post("/api/auth/login", json={"email": "admin@pricetracker.com", "password": "wrong"}).status_code == 401
    headers = auth(client)
    assert client.get("/api/auth/me", headers=headers).status_code == 200
    assert client.post("/api/auth/logout", headers=headers).status_code == 200


def test_catalog_crud_and_validation(client):
    headers, store, product = catalog(client)
    assert client.get("/api/stores", headers=headers).json[0]["id"] == store["id"]
    assert client.get("/api/products?search=Produto", headers=headers).json[0]["id"] == product["id"]
    assert client.put(f"/api/products/{product['id']}", headers=headers, json={"current_price": 110}).status_code == 200
    assert client.post("/api/products", headers=headers, json={"store_id": store["id"], "name": "Inválido", "sku": "SKU-2", "current_price": 0}).status_code == 400


def test_price_change_lifecycle_and_metrics(client):
    headers, store, product = catalog(client)
    payload = {"store_id": store["id"], "product_id": product["id"], "new_price": 125, "effective_date": (datetime.utcnow() + timedelta(days=1)).isoformat(), "reason": "Teste"}
    created = client.post("/api/price-changes", headers=headers, json=payload)
    assert created.status_code == 201
    change_id = created.json["data"]["id"]
    assert created.json["data"]["price_difference"] == 25
    assert created.json["data"]["percentage_change"] == 25
    assert client.post(f"/api/price-changes/{change_id}/execute", headers=headers).status_code == 400
    assert client.post(f"/api/price-changes/{change_id}/activate", headers=headers).status_code == 200
    assert client.post(f"/api/price-changes/{change_id}/execute", headers=headers).status_code == 200
    updated = client.get(f"/api/products/{product['id']}", headers=headers).json
    assert updated["current_price"] == 125
    assert client.put(f"/api/price-changes/{change_id}", headers=headers, json={"new_price": 150}).status_code == 400
    assert client.delete(f"/api/price-changes/{change_id}", headers=headers).status_code == 400
    dashboard = client.get("/api/dashboard", headers=headers).json
    assert dashboard["executed"] == 1
    assert "today_changes" in dashboard
    assert "largest_increases" in dashboard
    assert "largest_reductions" in dashboard


def test_price_change_filters_and_cancel(client):
    headers, store, product = catalog(client)
    payload = {"store_id": store["id"], "product_id": product["id"], "new_price": 90, "effective_date": datetime.utcnow().isoformat()}
    change_id = client.post("/api/price-changes", headers=headers, json=payload).json["data"]["id"]
    assert client.get("/api/price-changes?status=pending", headers=headers).json["total"] == 1
    assert client.get(f"/api/price-changes?store_id={store['id']}&product_id={product['id']}", headers=headers).json["total"] == 1
    assert client.put(f"/api/price-changes/{change_id}", headers=headers, json={"reason": "ajuste"}).status_code == 200
    assert client.delete(f"/api/price-changes/{change_id}", headers=headers).status_code == 200
    assert client.get("/api/price-changes?status=cancelled", headers=headers).json["total"] == 1


def test_full_catalog_delete_and_error_contract(client):
    headers, store, product = catalog(client)
    assert client.get(f"/api/stores/{store['id']}", headers=headers).status_code == 200
    assert client.get(f"/api/products/{product['id']}", headers=headers).status_code == 200
    assert client.get("/api/stores/missing", headers=headers).status_code == 404
    assert client.get("/api/products/missing", headers=headers).status_code == 404
    assert client.delete(f"/api/products/{product['id']}", headers=headers).status_code == 200
    assert client.delete(f"/api/stores/{store['id']}", headers=headers).status_code == 200


def test_active_cancel_and_pagination(client):
    headers, store, product = catalog(client)
    payload = {"store_id": store["id"], "product_id": product["id"], "new_price": 130, "effective_date": datetime.utcnow().isoformat()}
    change_id = client.post("/api/price-changes", headers=headers, json=payload).json["data"]["id"]
    assert client.post(f"/api/price-changes/{change_id}/activate", headers=headers).status_code == 200
    assert client.delete(f"/api/price-changes/{change_id}", headers=headers).status_code == 200
    assert client.delete(f"/api/price-changes/{change_id}", headers=headers).status_code == 400
    response = client.get("/api/price-changes?page=1&per_page=1", headers=headers)
    assert response.status_code == 200
    assert response.json["page"] == 1
    assert response.json["per_page"] == 1


def test_automation_executes_due_active_change_and_audits(client):
    headers, store, product = catalog(client)
    payload = {"store_id": store["id"], "product_id": product["id"], "new_price": 80, "effective_date": (datetime.utcnow() - timedelta(minutes=1)).isoformat()}
    change = client.post("/api/price-changes", headers=headers, json=payload).json["data"]
    assert client.post(f"/api/price-changes/{change['id']}/activate", headers=headers).status_code == 200
    result = client.post("/api/automation/run", headers=headers)
    assert result.status_code == 200
    assert result.json["processed"] == 1
    assert client.get(f"/api/products/{product['id']}", headers=headers).json["current_price"] == 80
    logs = client.get("/api/execution-logs", headers=headers)
    assert logs.status_code == 200
    assert logs.json[0]["status"] == "success"


def test_operational_endpoints_and_security_headers(client):
    assert client.get("/health/ready").status_code == 200
    metrics = client.get("/metrics")
    assert metrics.status_code == 200
    assert "stores_total" in metrics.json
    assert client.get("/health").headers["X-Content-Type-Options"] == "nosniff"


def test_product_history_details_and_sku_uniqueness(client):
    headers, store, product = catalog(client)
    payload = {"store_id": store["id"], "product_id": product["id"], "new_price": 140, "effective_date": datetime.utcnow().isoformat(), "reason": "Histórico"}
    assert client.post("/api/price-changes", headers=headers, json=payload).status_code == 201
    history = client.get(f"/api/products/{product['id']}/history", headers=headers)
    assert history.status_code == 200
    assert history.json["product"]["id"] == product["id"]
    assert history.json["total"] == 1
    duplicate = client.post("/api/products", headers=headers, json={"store_id": store["id"], "name": "Duplicado", "sku": "SKU-1", "current_price": 20})
    assert duplicate.status_code == 409
    assert client.get("/api/products/missing/history", headers=headers).status_code == 404
