from models import User

def test_creat_user():
    user = User(
        username='test',
        email='test@test',
        password='secret'
    )


    assert user.username == 'test'