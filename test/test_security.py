from http import HTTPStatus
from jwt import decode

from security import create_acess_token, SECRET_KEY, ALGORITHM


def test_jwt():
    data = {'test': 'test'}
    
    token = create_acess_token(data)

    decoded = decode(token, SECRET_KEY, algorithms=ALGORITHM)

    assert decoded['test'] == data['test']
    assert 'exp' in decoded

def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', 
        headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
