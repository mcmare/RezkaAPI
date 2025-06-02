from typing import Optional
import bcrypt
from fastapi import FastAPI, HTTPException
from fastapi.params import Query
from pydantic import BaseModel, EmailStr, Field
import uvicorn
from parser import get_main_category, get_main_subcategory, get_list_in_category, get_collections, search_content, \
    details, get_translate
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

@app.get("/subcategories/{cat_id}", summary="Подкатегории в основном меню", tags=["Категории"])
def get_menu_subcategory(cat_id: int):
    subcategories = get_main_subcategory(cat_id)
    return subcategories


@app.get("/list_in_category/{cat_id}/{pages}", summary="Вывод списка в категории", tags=["Список"])
def get_list_items(cat_id: int, pages: int):
    if pages:
        list_items = get_list_in_category(cat_id, pages)
    else:
        list_items = get_list_in_category(cat_id)
    return list_items

@app.get("/list_collections", summary="Вывод списка коллекций", tags=["Список"])
def get_list_collections(pages: Optional[int] = 1):
    list_collections = get_collections(pages)
    return list_collections

@app.get("/search", summary="Вывод списка из поиска", tags=["Список"])
def get_list_in_search(query: Optional[str] = None, pages: Optional[int] = 1):
    return search_content(query, pages)

@app.get("/details", summary="Вывод информации о фильме", tags=["Детали"])
def get_details(id: int):
    return details(id)

@app.get("/translates", summary="Вывод списка переводов", tags=["Детали"])
def get_translates(id: int):
    return get_translate(id)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
