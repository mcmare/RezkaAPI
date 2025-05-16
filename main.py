import bcrypt
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
import uvicorn
from parser import get_main_category
from database import create_user
app = FastAPI()

users = []


@app.post("/create-db", summary="Удаляет и создает базу данных", tags=["База данных"])
def create_db():
    return {"ok": True, "msg": "Базы данных успешно удалены и созданы по новой"}


@app.get("/users", summary="Вывод всех пользователей", tags=["Пользователи"])
def get_users():
    return users


@app.post("/add_user", summary="добавить пользователя", tags=["Пользователи"])
def add_user(username, password):
    # Хешируем и солим пароль
    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    create_user(username, password)
    return {"ok": True, "msg": "Пользователь добавлен", "username": username, "password": password}


@app.get("/categories", summary="Основные категории меню", tags=["Категории"])
def get_menu_categories():
    categories = get_main_category()
    return categories


@app.get("/categories/{id}", summary="Название и ссылка на основные категории меню", tags=["Категории"])
def get_menu_category(id: int):
    categories = get_menu_categories()
    for n in categories:
        if n["id"] == id:
            return n
    raise HTTPException(status_code=404, detail="Категория не найдена")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
