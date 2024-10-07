from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    # Простая логика авторизации
    if username == "admin" and password == "password":
        request.session['user'] = username
        return {"message": "Login successful"}
    return {"message": "Invalid credentials"}

@router.post("/logout")
async def logout(request: Request):
    request.session.clear()
    return {"message": "Logged out"}
