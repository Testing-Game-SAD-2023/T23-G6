from logic import Logic
from fastapi.responses import JSONResponse

class Presentation :

    def RegistraGiocatore(json: dict) -> JSONResponse:
        return Logic.User.signUp(json)

    def LoginGiocatore(json: dict) -> JSONResponse:
        return Logic.User.login(json)

    def LogOut(token: str) -> JSONResponse:
        return Logic.User.logOut(token)

    def InviaNuovaEmail(token: str) -> JSONResponse:
        return Logic.User.sendNewEmail(token)

    def Redirect(json : dict, token : str) -> JSONResponse:
        return Logic.Redirect(json, token)

    def ConfermaEmail(json: dict, token: str) -> JSONResponse:
        return Logic.User.confirmEmail(json, token)

    def RecuperaAccountInviaEmail(json : dict) -> JSONResponse:
        return Logic.User.sendEmailRecoverAccount(json)

    def RecuperaAccountCambiaPassword(json : dict) -> JSONResponse:
        return Logic.User.changePasswordRecoverAccount(json)

    def OttieniDatiUtente(token : str) -> JSONResponse:
        return Logic.User.getUserData(token)