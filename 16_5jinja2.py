from fastapi import FastAPI,status, Body, HTTPException, Path, Request, Form
from fastapi.responses import HTMLResponse
from typing import Annotated, List
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel # Импорт моделей Pydantic (для валидации входящих и исходящих данных)


app = FastAPI()
templates = Jinja2Templates(directory="templates") #объект Jinja2Templates, папка шаблонов - templates

# Создайте пустой список
users = []

# Создание класса(модели) User, от класса BaseModel. Pydantic
class User(BaseModel):
    id: int
    username: str
    age: int



@app.get("/")
async def get_main_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.get(path='/user/{user_id}')
async def get_users(request: Request, user_id: int) -> HTMLResponse:
            return templates.TemplateResponse("users.html", {"request": request, "user": users[user_id]})


@app.post('/user/{username}/{age}')
async def post_user(
        username: Annotated[str,
            Path(max_length=35, description='Введите имя', example='Alex')],
        age: Annotated[int,
            Path(le=100, description='Введите возраст', example='25')]):
    user_id = len(users) + 1
    user = User(id=user_id, username=username, age=age)
    users.append(user)
    return f'Пользователь {user.username} id={user.id} возраст {user.age} зарегестрирован'

@app.put('/user/{user_id}/{username}/{age}')
async def put_user(user_id: Annotated[int, Path(description='Введите ID', example='1')],
                   username: Annotated[str, Path(max_length=35, description='Введите имя', example='Alex')],
                   age: Annotated[int, Path(le=100, description='Введите возраст', example='25')]):
    for i in users:
        if i.id == user_id:
            i.username = username
            i.age = age
        return users  # возвращает обновленный список
    # исключение в случае отсутствия пользователя с введенным id
    raise HTTPException(status_code=404, detail="Пользователь не найден")


@app.delete("/user/{user_id}")
def delete_user(user_id: Annotated[int, Path(description='Введите ID', example='1')]):
    for i, user in enumerate(users):
        if user.id == user_id:
            # удаление записи в списке users по найденному id
            del users[i]
            return users # возврат измененный список users
    # исключение в случае отсутствия пользователя с введенным id
    raise HTTPException(status_code=404, detail=f"Пользователь с ID {user_id} отсутствует")