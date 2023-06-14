import time
import smtplib
import configparser
from model import Model
from fastapi.responses import JSONResponse
import re
from sqlalchemy import exc

# TODO: gestire eccezioni
class Controller:

    def Redirect(json : dict, token : str) -> JSONResponse:
        print(token)
        redirectSettings = Model.Redirect.getSettings()
        try:
            session = Model.Session(user_token = token)
            if session.user_token != None and len(session.search()) == 0:
                raise exc.InvalidRequestError('The token is not valid')

            loc = json['LOC']
            if session.user_token == None:
                if loc in redirectSettings["privatePages"]:
                    redirectPage = redirectSettings["notLoggedRedirect"]
                else:
                    redirectPage = loc
            elif session.user_token[-1] == Controller.Session.ConfirmPasswordFinalCharacter:
                if loc == redirectSettings["confirmationPage"]:
                    redirectPage = loc
                else:
                    redirectPage = redirectSettings["confirmationPage"]
            else:
                if (loc in redirectSettings["publicPages"]) or (loc in redirectSettings["confirmationPage"]):
                    redirectPage = redirectSettings["LoggedRedirect"]
                else:
                    redirectPage = loc

            res = JSONResponse({'MSG': "Success", "REDIRECT" : redirectPage})
            return res
        except exc.InvalidRequestError as e:
            res = JSONResponse({'MSG': e})
            res.delete_cookie(key='TOKEN', samesite='none', secure=True)
            return res

    class User:

        def signUp(json: dict) -> JSONResponse:
            try:
                if not Controller.User.__checkDataIntegrity(json):
                    raise ValueError("Invalid User data")

                newUser = Model.User(json = json, cript = True)
                newUser.registration_state = Controller.Session.generateEmailCode(newUser.email)
                newUser.insert()

                subject = "Subject: Confirm your CodeDefender's account\n\n"
                payload = "Login and type the following code to complete your registration : "
                Controller.Email.sendEmail(newUser.email, subject, payload, newUser.registration_state)

                res = JSONResponse({'MSG': "Success"})
                return res
            
            except ValueError:
                res = JSONResponse({'MSG': "Invalid User data"})
                return res
            except exc.InvalidRequestError:
                res = JSONResponse({'MSG': "Invalid request"})
                return res
            except smtplib.SMTPException:
                res = JSONResponse({'MSG': "Could not send email"})
                return res


        def login(json: dict) -> JSONResponse:
            try:
                loggedUser = Model.User(json = json, cript = True).search()[0]
                token = Controller.Session.generateLoginToken(loggedUser.email, loggedUser.registration_state)

                if (len(loggedUser.registration_state) > 1 and 
                    loggedUser.registration_state[-1] == Controller.Session.RecoverAccountFinalCharacter):
                    raise ConnectionRefusedError('Could not login because the user have asked for recovery account')
                
                session = Model.Session(user_token = token, id_user = loggedUser.id)
                session.insert()

                redirectSettings = Model.Redirect.getSettings()

                if len(loggedUser.registration_state) > 0:
                    redirectPage = redirectSettings['confirmationPage']
                else:
                    redirectPage = redirectSettings['LoggedRedirect']

                res = JSONResponse({'MSG': "Success", 'REDIRECT': redirectPage})
                res.set_cookie("TOKEN", session.user_token, samesite='none', secure=True)
                return res
            
            except IndexError:
                res = JSONResponse({'MSG': "Invalid credentials"})
                return res
            except exc.InvalidRequestError: # Impossibile inserire il token
                res = JSONResponse({'MSG': "Invalid request"})
                return res
            except ConnectionRefusedError: # Impossibile loggare un account che ha chiesto il recupero password
                res = JSONResponse({'MSG': "Could not login because the user have asked for recovery account"})
                return res

        #Non implementato
        def sendNewEmail(token: str) -> JSONResponse:
            user = Model.User(registration_state = token)
            user = user.search()[0]
            if user.registration_state[-1] == 'f':
                subject = "Subject: Confirm your CodeDefenders' account\n\n"
                payload = "Login and type the following code to complete your registration : "
                Controller.Email.sendEmail(user.email, subject, payload, user.registration_state)
                res = JSONResponse({'MSG': "Success"})
            else:
                res = JSONResponse({'MSG': "Account already confirmed"})
            return res

        def logOut(token: str) -> JSONResponse:
            try:
                session = Model.Session(user_token = token)
                session.delete()

                redirectPage = Model.Redirect.getSettings()['notLoggedRedirect']
                res = JSONResponse(content={"MSG": "Success", 'REDIRECT': redirectPage})
                res.delete_cookie(key='TOKEN', samesite='none', secure=True)
                return res
            except exc.InvalidRequestError:
                res = JSONResponse({'MSG': "Could not delete the session"})
                return res

        def confirmEmail(json : dict, token : str) -> JSONResponse:
            try:
                session = Model.Session(user_token = token).search()[0]

                user = Model.User(id = session.id_user, cript = True).search()[0]
                user.update(REGISTRATION_STATE = "")
                session.delete()
                
                session = Model.Session(user_token = Controller.Session.generateLoginToken(user.email, ""), id_user = user.id)
                session.insert()

                redirectPage = Model.Redirect.getSettings()['LoggedRedirect']
                res = JSONResponse({'MSG': "Success", 'REDIRECT': redirectPage})
                res.set_cookie("TOKEN", session.user_token, samesite='none', secure=True)
                return res
            
            except IndexError:
                res = JSONResponse({'MSG': "Confirmation failed"})
                return res
            except exc.InvalidRequestError:
                res = JSONResponse({'MSG': "Invalid request"})
                return res

        def sendEmailRecoverAccount(json : dict) -> JSONResponse:
            try:
                user = Model.User(json)
                user = user.search()[0]

                code = Controller.Session.generateNewPasswordCode(user.email)
                user.update(REGISTRATION_STATE = code)

                subject = "Subject: Recover your CodeDefenders' Account\n\n"
                payload = "Here it is the code you need to set a new password: "
                Controller.Email.sendEmail(user.email, subject, payload, code)
                res = JSONResponse({'MSG': "Success"})
                return res
            
            except IndexError:
                res = JSONResponse({'MSG': "Unregistered email"})
                return res 
            except exc.InvalidRequestError:
                res = JSONResponse({'MSG': "Invalid request"})
                return res 
            except smtplib.SMTPException:
                res = JSONResponse({'MSG': "Could not send email"})
                return res
        
        def changePasswordRecoverAccount(json : dict) -> JSONResponse:
            try:
                user = Model.User(registration_state = json['CODE'], cript = True)
                user = user.search()[0]
                user.update(PW = json['PW'], REGISTRATION_STATE = "")
                res = JSONResponse({'MSG': "Success"})
                return res
            
            except IndexError:
                res = JSONResponse({'MSG': "The code is invalid"})
                return res
            except exc.InvalidRequestError:
                res = JSONResponse({'MSG': "Invalid request"})
                return res


        def __checkDataIntegrity(json : dict) -> bool:
            expectedKeys = ['NAME','SURNAME','EMAIL','PW', 'DEGREE']
            receivedKeys = list(json.keys())

            if len(list(set(expectedKeys) - set(receivedKeys))) == 0:
                if ((re.match(r"^[A-Za-z\s]+$", json['NAME']) is not None) and
                    (re.match(r"^[A-Za-z\s]+$", json['SURNAME']) is not None) and
                    (re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", json['EMAIL']) is not None) and
                    (re.match(r"^[A-Za-z0-9]{7,32}$", json['PW']) is not None)):
                    return True
                return False

        def getUserData(token : str) -> JSONResponse:
            try:
                session = Model.Session(user_token = token).search()[0]
                user = Model.User(id = session.id_user, cript = True).search()[0]
                res = {}
                res['MSG'] = 'Success'
                res['name'] = user.name
                res['surname'] = user.surname
                res['email'] = user.email
                res['degree'] = user.degree
                return JSONResponse(res)
            
            except exc.InvalidRequestError:
                return JSONResponse({'MSG': "Invalid request"})
            
    class Session:

        ConfirmPasswordFinalCharacter : str = "C"
        RecoverAccountFinalCharacter : str = "R"
        LoggedUserFinalCharacter : str = "V"

        def generateEmailCode(email: str, len=10) -> str:
            return Model.Session.generateToken(email, time.ctime())[0:len] + Controller.Session.ConfirmPasswordFinalCharacter
        
        def generateNewPasswordCode(email: str, len=10) -> str:
            return Model.Session.generateToken(email, time.ctime())[0:len] + Controller.Session.RecoverAccountFinalCharacter

        def generateLoginToken(email: str, registrationState: str):
            while True:
                token = Model.Session.generateToken(email, time.ctime())

                if len(registrationState) > 0:
                    token = token + Controller.Session.ConfirmPasswordFinalCharacter
                else:
                    token = token + Controller.Session.LoggedUserFinalCharacter

                if len(Model.Session(user_token = token).search()) == 0:
                    break
            return token

    class Email:
        username = None
        password = None
        STMPServer = None
        port = None

        def sendEmail(addressee: str, subject : str, payload : str, token: str):
            if Controller.Email.username is None or\
                Controller.Email.password is None or\
                Controller.Email.STMPServer is None or\
                Controller.Email.port is None:
                Controller.Email.__initEmailSettings__()

            try:
                msg = subject + payload + token
                email = smtplib.SMTP(Controller.Email.STMPServer, Controller.Email.port)
                email.ehlo()
                email.starttls()
                email.login(Controller.Email.username, Controller.Email.password)
                email.sendmail(Controller.Email.username,addressee, msg.encode('utf-8'))
                email.quit()
            except:
                raise smtplib.SMTPException('Could not send email')

        def __initEmailSettings__():
            config = configparser.ConfigParser()
            config.read('settings/utils.ini')
            #password = "progettosad6!"
            Controller.Email.username = config['EmailSettings']['username']
            Controller.Email.password = config['EmailSettings']['password']
            Controller.Email.STMPServer = config['EmailSettings']['STMPServer']
            Controller.Email.port = config['EmailSettings']['port']
