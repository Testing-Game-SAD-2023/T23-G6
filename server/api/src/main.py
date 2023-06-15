from fastapi import FastAPI, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware
from presentation import Presentation

app = FastAPI()

origins = ["http://127.0.0.1"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex='http://127.0.0.1.*',
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
    max_age=3600
)

prefix_router = APIRouter(prefix="/api")


@prefix_router.post("/RegistraGiocatore")
async def RegistraGiocatore(request: Request):
    return Presentation.RegistraGiocatore(await request.json())


@prefix_router.post("/LoginGiocatore")
async def LoginGiocatore(request: Request):
    return Presentation.LoginGiocatore(await request.json())


@prefix_router.post("/InviaNuovaEmail")
async def InviaNuovaEmail(request: Request):
    return Presentation.InviaNuovaEmail(request.cookies.get('TOKEN'))


@prefix_router.post("/LogOut")
async def LogOut(request: Request):
    return Presentation.LogOut(request.cookies.get('TOKEN'))


@prefix_router.post("/Redirect")
async def Redirect(request: Request):
    return Presentation.Redirect(await request.json(), request.cookies.get('TOKEN'))


@prefix_router.post("/ConfermaEmail")
async def ConfermaEmail(request: Request):
    return Presentation.ConfermaEmail(await request.json(), request.cookies.get('TOKEN'))


@prefix_router.post("/RecuperaAccountInviaEmail")
async def RecuperaAccountInviaEmail(request: Request):
    return Presentation.RecuperaAccountInviaEmail(await request.json())

@prefix_router.post("/RecuperaAccountCambiaPassword")
async def RecuperaAccountCambiaPassword(request: Request):
    return Presentation.RecuperaAccountCambiaPassword(await request.json())

@prefix_router.post("/OttieniDatiUtente")
async def OttieniDatiUtente(request: Request):
    return Presentation.OttieniDatiUtente(request.cookies.get('TOKEN'))

app.include_router(prefix_router)