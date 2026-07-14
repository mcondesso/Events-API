from models import User


def test_user_password_hashing_behaves_correctly():
    # Arrange: create new user
    user = User(username="username", is_admin=False)

    password = "pass1234"

    # Act: set password
    user.set_password(password)

    # Assert
    assert user.password_hash != password
    assert user.check_password(password)
    assert user.is_admin == False
