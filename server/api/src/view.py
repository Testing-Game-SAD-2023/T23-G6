from controller import Controller
from fastapi.responses import JSONResponse

class View :

    def RegistraGiocatore(json: dict) -> JSONResponse:
        return Controller.User.signUp(json)

    def LoginGiocatore(json: dict) -> JSONResponse:
        return Controller.User.login(json)

    def LogOut(token: str) -> JSONResponse:
        return Controller.User.logOut(token)

    def InviaNuovaEmail(token: str) -> JSONResponse:
        return Controller.User.sendNewEmail(token)

    def Redirect(json : dict, token : str) -> JSONResponse:
        return Controller.Redirect(json, token)

    def ConfermaEmail(json: dict, token: str) -> JSONResponse:
        return Controller.User.confirmEmail(json, token)

    def RecuperaAccountInviaEmail(json : dict) -> JSONResponse:
        return Controller.User.sendEmailRecoverAccount(json)
    
    def RecuperaAccountCambiaPassword(json : dict) -> JSONResponse:
        return Controller.User.changePasswordRecoverAccount(json)