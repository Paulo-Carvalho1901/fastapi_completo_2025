from jwt import decode


from security import create_acess_token, SECRET_KEY, ALGORITHM


def test_jwt():
    data = {'test': 'test'}
    
    token = create_acess_token(data)

    decoded = decode(token, SECRET_KEY, algorithms=ALGORITHM)

    assert decoded['test'] == data['test']
    assert 'exp' in decoded
