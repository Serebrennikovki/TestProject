from decimal import Decimal

from fastapi import APIRouter, Request, Form, Depends, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from DTO.user_create import UserCreate
from DTO.deposit_balance import DepositBalance
from DTO.ml_task_create_request import MlTaskCreateRequest
from core.exceptions import UserError
from database.database import get_session
from services.repositories import user as UserRepository
from core.authenticate import authenticate_cookie
from core import security as SecurityService
from core.jwt_handler import create_access_token
from database.config import get_settings
from services.business_logic import balance as BalanceService
from services.business_logic import history as HistoryService
from services.business_logic import user as UserService
from services.business_logic import prediction as PredictService


web_router = APIRouter()
templates = Jinja2Templates(directory="templates")
settings = get_settings()

@web_router.get("/")
async def index(
    request: Request
):
    return templates.TemplateResponse(request, "index.html")

# ── Страница логина ──────────────────────────────────────────────────────────

@web_router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html")

@web_router.post("/ui/login")
async def ui_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    session=Depends(get_session)
):
    user = UserRepository.get_user_by_login(login=username, session=session)
    if not user:
        return templates.TemplateResponse(
            request,
            "login.html",
            {"request": request, "error": "Неверный логин или пароль"},
            status_code=401,
        )
    if SecurityService.verify_password(password=password, hashed_password=user.password):
        token = create_access_token(user=username)
        response = RedirectResponse(url="/dashboard", status_code=303)
        response.set_cookie(
            key=settings.COOKIE_NAME, 
            value=f"Bearer {token}", 
            httponly=True
        )
        
        return response

# ── Регистрация ──────────────────────────────────────────────────────────────

@web_router.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse(request, name="register.html")

@web_router.post("/ui/register")
async def ui_register(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    name: str = Form(...),
    session=Depends(get_session)
):
    try:
        user = UserCreate(login=username, password=password,name=name)
        user = UserService.create_user(data=user, session=session)
    except UserError as e:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": str(e)},
            status_code=400,
        )
    return RedirectResponse(f'/login', status_code=303)

# ── Личный кабинет ───────────────────────────────────────────────────────────

@web_router.get("/dashboard")
async def dashboard(
    request: Request,
    user_login=Depends(authenticate_cookie),
    session=Depends(get_session)):

    user    = UserRepository.get_user_by_login(login=user_login, session=session)
    balance = BalanceService.get_balance(user_login, session)
    history = HistoryService.get_history(user_login, session)
    mlHistory = PredictService.get_all_task( user_login, session)

    return templates.TemplateResponse(request, "dashboard.html", {
        "request": request,
        "user": user,
        "balance": balance,
        "history": history,
        "mlHistory": mlHistory
    })
# ── Выход ────────────────────────────────────────────────────────────────────

@web_router.post("/balance/deposit")
async def dashboard(
    request: Request,
    amount: Decimal= Form(...),
    user_login=Depends(authenticate_cookie),
    session=Depends(get_session)):

    balance = DepositBalance(user_login=user_login, amount=amount)
    BalanceService.add_deposit(balance, session)
    return RedirectResponse(url="/dashboard", status_code=303)

@web_router.post("/predict")
async def dashboard(
    request: Request,
    prompt: str= Form(...),
    user_login=Depends(authenticate_cookie),
    session=Depends(get_session)):

    reqMl = MlTaskCreateRequest(user_login=user_login, input_data=prompt)
    PredictService.add_prediction(data=reqMl, session=session)
    return RedirectResponse(url="/dashboard", status_code=303)

# ── Выход ────────────────────────────────────────────────────────────────────

@web_router.post("/ui/logout")
async def logout():
    response = RedirectResponse("/login", status_code=303)
    response.delete_cookie("access_token")
    return response