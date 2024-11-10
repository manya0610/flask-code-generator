from models import User, db


def get_all_user():
    return User.query.all()


def get_user(id):
    return User.query.filter(User.id == id).one_or_none()


def create_user(name, email, password):
    return User(name, email, password)


def update_user(id, **kwargs):
    user = get_user(id)
    if not user:
        raise Exception("Not Found")
    for attr, value in kwargs.items():
        setattr(user, attr, value)
    db.session.commit()
    return user


def delete_user(id):
    user = get_user(id)
    if not user:
        raise Exception("Not Found")
    db.session.delete(user)
    db.session.commit()
