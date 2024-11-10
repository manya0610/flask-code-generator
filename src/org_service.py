from models import Org, db


def get_all_org():
    return Org.query.all()


def get_org(id):
    return Org.query.filter(Org.id == id).one_or_none()


def create_org(name, public_id):
    return Org(name, public_id)


def update_org(id, **kwargs):
    org = get_org(id)
    if not org:
        raise Exception("Not Found")
    for attr, value in kwargs.items():
        setattr(org, attr, value)
    db.session.commit()
    return org


def delete_org(id):
    org = get_org(id)
    if not org:
        raise Exception("Not Found")
    db.session.delete(org)
    db.session.commit()
