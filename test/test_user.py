from http import HTTPStatus



def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'password': 'strong_password',
            'email': 'alice@hotmail.com'
        }
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'email': 'alice@hotmail.com',
        'username': 'alice'
    }
    
def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
             {
                'id': 1,
                'email': 'alice@hotmail.com',
                'username': 'alice',
            }
        ]
    }

def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username':'bob',
            'email': 'bob@hotmail.com',
            'password': 'secrets'
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username':'bob',
            'email': 'bob@hotmail.com',
            'id': 1
    }

def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username':'bob',
            'email': 'bob@hotmail.com',
            'id': 1
    }
