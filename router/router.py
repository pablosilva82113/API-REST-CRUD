from fastapi import APIRouter , Response
from starlette.status import HTTP_201_CREATED , HTTP_204_NO_CONTENT
from schemas.user_schema import User_schema , DataUser
from config.db import engine
from model.users import users
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash , check_password_hash
from typing import List

user = APIRouter()

#ruta raiz
@user.get('/')
def root():
    return {'message': 'Hi router'}

#ruta para obtener usuarios
#get = obtener usuarios
@user.get('/api/users', response_model=List[User_schema])
def get_users():
    try:
      with engine.connect() as conn:
        resul = conn.execute(users.select()).fetchall()
        users_list = []
        for i in resul:
            user_dict = {
                'id': i[0],
                'name': i[1],
                'usname': i[2],
                'passw': i[3]}
            users_list.append(user_dict)
        
        return users_list
    except SQLAlchemyError as e:
        print(f"Error al solictar en la base de datos: {str(e)}")
        return 'Error '

#ruta para obtener un usuario por id
@user.get('/api/user/{id}',response_model=User_schema)
def get_user(user_di:int):
    try:
        with engine.connect() as conn:
           resul = conn.execute(users.select().where(users.c.id ==user_di)).first()
        return resul
    except SQLAlchemyError as e:
        print(f"Error al solictar en la base de datos: {str(e)}")
        return 'Error '

#ruta para crear usuarios 
#post = crear usuarios o insertar
@user.post('/api/user' , status_code=HTTP_201_CREATED)
def create_user(data_user:User_schema):
    new_user = data_user.dict()
    try:
        with engine.connect() as conn:
            new_user['user_pass'] = generate_password_hash(data_user.user_pass,"pbkdf2:sha256:30",30)
            conn.execute(users.insert().values(new_user))
            conn.commit()
    except SQLAlchemyError as e:
        print(f"Error al crear en la base de datos: {str(e)}")
        return 'Error en la inserción'
    return Response(status_code=HTTP_201_CREATED)

@user.post('/api/user/login')
def user_login(user_data:DataUser):
    try:
      with engine.connect() as conn:
         result = conn.execute(users.select().where(users.c.username == user_data.username)).first()
         response =  { "username": result.username,"user_pass": result.user_pass}
         print(response)
         if result != None:
            check_pass = check_password_hash(result[3],user_data.user_pass)
            print(check_pass)
            return 'welcome'
         
    except:
      print('An exception occurred')
#ruta para actualizar usuarios
#put = actualizar usuarios o modificar
@user.put('/api/user/{id}',response_model=User_schema)
def update_user(data_user:User_schema,user_di:int):
    try:
      with engine.connect() as conn:
        encryp_paasword = generate_password_hash(data_user.user_pass,"pbkdf2:sha256:30",30)
        conn.execute(users.update().values(name=data_user.name,username=data_user.username,
                                           user_pass=encryp_paasword).where(users.c.id == user_di))
        
        result = conn.execute(users.select().where(users.c.id == user_di)).first()
        conn.commit()
        response =  {"id": result.id, "name": result.name, "username": result.username}
        return response
    except SQLAlchemyError as e:
        print(f"Error al actualizar en la base de datos: {str(e)}")
        return 'Error en la actualizacion'

# ruta para eliminar usuarios
# delete = eliminar usuarios o borrar   
@user.delete('/api/user/{id}',status_code=HTTP_204_NO_CONTENT)
def delete_user(user_di:int):
    try:
       with engine.connect() as conn:
          conn.execute(users.delete().where(users.c.id == user_di))
          conn.commit()
          return Response(status_code=HTTP_204_NO_CONTENT)
    except SQLAlchemyError as e:
        print(f"Error al eliminar en la base de datos: {str(e)}")
        return 'Error al elimiar '