from sqlalchemy.orm import Session

from . import models, schemas

# TODO: Refactorizar esta función para varios parámetros
def get_user(db: Session, username: str = None, email: str = None, id: int = None):
    if username:
        return db.query(models.User).filter(models.User.username == username).first()
    elif email:    
        return db.query(models.User).filter(models.User.email == email).first()
    elif id:    
        return db.query(models.User).filter(models.User.id == id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username = user.username, name = user.name, 
                            email = user.email, group_id = user.group_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_groups(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Group).offset(skip).limit(limit).all()


def get_group(db: Session, name_group):
    return db.query(models.Group).filter(models.Group.name_group == name_group).first()


def get_group_id(db: Session, id: int):
    return db.query(models.Group).filter(models.Group.id == id).first()


def create_group(db: Session, group=schemas.GroupCreate):
    db_group = models.Group(name_group = group.name_group, city = group.city, link = group.link)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group


def get_user_group(db: Session, group_id: int):
    return db.query(models.User).filter(models.User.group_id == group_id).all()


def update_user(db: Session, user_id: int, user: schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()

    db_user.username = user.username
    db_user.name = user.name
    db_user.email = user.email
    db_user.group_id = user.group_id

    db.commit()
    db.refresh(db_user)

    return db_user


def update_group(db: Session, group_id: int, group: schemas.GroupCreate):
    db_group = db.query(models.Group).filter(models.Group.id == group_id).first()

    db_group.name_group = group.name_group
    db_group.city = group.city
    db_group.link = group.link

    db.commit()
    db.refresh(db_group)

    return db_group



def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    
    return db_user



if __name__ == "__main__":
    pass