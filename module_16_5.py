from fastapi import FastAPI, HTTPException, Path, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()
templates = Jinja2Templates(directory="templates")

users = []
user_id_counter = 1

class User(BaseModel):
    id: int
    username: str
    age: int

@app.get("/", response_class=HTMLResponse)
def read_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.get("/user/{user_id}", response_class=HTMLResponse)
def get_user(request: Request, user_id: int):
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse("users.html", {"request": request, "user": user})
    raise HTTPException(status_code=404, detail='User was not found')

@app.post('/user/{username}/{age}')
def create_user(
    username: Annotated[str, Path(description='Enter username', min_length=5, max_length=20, example='UrbanUser')],
    age: Annotated[int, Path(description='Enter age', ge=18, le=120, example=24)]
) -> User:
    global user_id_counter
    user_id = user_id_counter
    user_id_counter += 1
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user

@app.put('/user/{user_id}/{username}/{age}')
def update_user(user_id: int = Path(..., description='Enter User ID', ge=1, le=100, example=1),
                username: str = Path(..., description='Enter username', min_length=5, max_length=20,
                                     example='UrbanProfi'),
                age: int = Path(..., description='Enter age', ge=18, le=120, example=28)
                ) -> User:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail='User was not found')

@app.delete("/user/{user_id}", response_model=User)
async def delete_user(user_id: int = Path(..., description='Enter User ID', ge=1, le=100, example=2)) -> User:
    for i, user in enumerate(users):
        if user.id == user_id:
            return users.pop(i)
    raise HTTPException(status_code=404, detail="User was not found")