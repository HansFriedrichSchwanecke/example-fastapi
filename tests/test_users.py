from app import schemas


def test_root(client):
    res = client.get("/")
    # print(res.json().get('message'))
    assert res.json().get('message') == 'Hello World'
    assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/users", json={"email": "hello1352@mytum.de", "password": "password123"})
    new_user = schemas.UserOut(**res.json())

    assert new_user.email == "hello1352@mytum.de"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post(
        "/login/", data={"username": test_user['email'], "password": test_user['password']})

    assert res.status_code == 200
