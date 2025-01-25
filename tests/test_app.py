def test_homepage(client):
    res = client.get("/")
    assert b'<!doctype html>' in res.data
