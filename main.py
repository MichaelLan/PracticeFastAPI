#coding: utf-8

from typing import List
from fastapi import FastAPI, Path, Query, Depends, HTTPException
from sqlalchemy.orm import Session

from databases import crud, models, schemas
from databases.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


#------------------------------------------------------------------
@app.get('/users/', response_model=List[schemas.User]) # Ready
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Obtener todos los usuarios
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users


#------------------------------------------------------------------
@app.post('/users/', response_model=schemas.User) # Ready
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Crear un usuario
    db_user = crud.get_user(db, username = user.username)
    db_email = crud.get_user(db,  email= user.email)
    db_group = crud.get_group_id(db=db, id=user.group_id)
    
    print(db_group)
    
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    if not db_group:
        raise HTTPException(status_code=400, detail="Group not found")

    return crud.create_user(db=db, user=user)


#------------------------------------------------------------------
@app.get('/groups/') # Ready
def get_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Obtener todos los grupos
    groups = crud.get_groups(db=db, skip=skip, limit=limit)
    return groups


#------------------------------------------------------------------
@app.post('/groups/') # Ready
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    # Crear un grupo
    db_group = crud.get_group(db, name_group = group.name_group)
    if db_group:
        raise HTTPException(status_code=400, detail='Name already exist')
    return crud.create_group(db=db, group=group)


#------------------------------------------------------------------
@app.get('/users/group/{group_id}/', response_model=List[schemas.User])
def get_users_groups(group_id: int, db: Session = Depends(get_db)):
    # Ready
    # Obtener los usuarios de un grupo
    users_group = crud.get_user_group(db=db, group_id=group_id)
    return users_group


#------------------------------------------------------------------
@app.get('/users/{user_id}/', response_model=schemas.User) # Ready
def get_user(user_id: int, db: Session = Depends(get_db)):
    # Obtener un usuario específico
    db_user = crud.get_user(db=db, id=user_id)
    return db_user


#------------------------------------------------------------------
@app.delete('/users/{user_id}/') # Ready
def delete_user(user_id: int, db: Session = Depends(get_db)):
    # Eliminar un usuario
    db_id = crud.get_user(db=db, id=user_id)
    if not db_id:
        raise HTTPException(status_code=400, detail='User not found')
    return crud.delete_user(db=db, user_id=user_id)


#------------------------------------------------------------------
@app.put('/users/{user_id}/') # Ready
def edit_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Editar un usuario

    username = user.username
    name = user.name
    email = user.email
    group_id = user.group_id

    db_username = crud.get_user(db=db, username=username)
    db_email = crud.get_user(db=db, email=email)
    db_group = crud.get_group_id(db=db, id=group_id)

    # TODO: hacer las validaciones para todos los demás 
    # usuarios, excepto para el que se está tratando de editar
    if db_username:
        raise HTTPException(status_code=400, detail='Username already registered')
    
    if db_email:
        raise HTTPException(status_code=400, detail='Email already registered')

    if not db_group:
        raise HTTPException(status_code=400, detail='Group not found')
    
    return crud.update_user(db=db, user_id=user_id, user=user)


#------------------------------------------------------------------
@app.put('/groups/{group_id}/', response_model=schemas.Group) # Ready
def edit_group(group_id: int, group: schemas.GroupCreate, db: Session = Depends(get_db)):
    # Editar un grupo
    name_group = crud.get_group(db=db, name_group=group.name_group)

    # TODO: hacer las validaciones para todos los demás 
    # usuarios, excepto para el que se está tratando de editar
    if name_group:
        raise HTTPException(status_code=400, detail='Name already registered')
    return crud.update_group(db=db, group_id=group_id, group=group)


#------------------------------------------------------------------
@app.delete('/users/{group_id}/')
def delete_users_group(group_id: int):
    # Eliminar todos los usuarios de un grupo
    pass


#------------------------------------------------------------------
@app.delete('/groups/{group_id}/')
def delete_group(group_id):
    #Eliminar un grupo y los usuarios asociados
    pass