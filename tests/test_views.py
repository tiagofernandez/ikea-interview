from warehouse.views import index


def test_index(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.mimetype == "text/html"


def test_health_check(client):
    endpoint = "health-check"
    for path in [f"{endpoint}", f"{endpoint}/"]:
        r = client.get(f"/api/{path}")
        assert r.status_code == 200
