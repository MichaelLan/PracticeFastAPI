from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(..., title='username')
    name: str = Field(..., title='Nombre')
    email: str = Field(..., title='Correo electrónico', regex='^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$')
    group_id: int = Field(..., title='ID del grupo al que pertenece')


class GroupBase(BaseModel):
    name_group: str = Field(..., title='Nombre del grupo')
    city: str
    link: str = None


class UserCreate(UserBase):
    pass


class GroupCreate(GroupBase):
    pass


class Group(GroupBase):
    # Para lectura
    id: int

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
        
    class Config:
        orm_mode = True

