from users.models import User


def get_unknown_user():
    return User.objects.get_or_create(username='unknown')[0]
