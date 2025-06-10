from dataclasses import asdict
from sqlalchemy import select
from datetime import datetime
from models import User


def test_creat_user(session, mock_db_time):

    with mock_db_time(model=User) as time:
        new_user = User(
            username='test',
            email='test@test',
            password='secret'
        )

        session.add(new_user)
        session.commit()

        user = session.scalar(
            select(User).where(User.username == 'test')
        )

    assert asdict(user) == {
        'id': 1,
        'username': 'test',
        'email': 'test@test',
        'password': 'secret',
        'created_at': time,
    }
