import time
import smtplib
import configparser
from data import Data
from fastapi.responses import JSONResponse
import re
from sqlalchemy import exc

class Logic:

    def Redirect(json : dict, token : str) -> JSONResponse:
        print(token)
        redirectSettings = Data.Redirect.getSettings()
        try:
            session = Data.Session(user_token = token)
            if session.user_token != None and len(session.search()) == 0:
                raise exc.InvalidRequestError('The token is not valid')

            loc = json['LOC']
            if session.user_token == None:
                if loc in redirectSettings["privatePages"]:
                    redirectPage = redirectSettings["notLoggedRedirect"]
                else:
                    redirectPage = loc
            elif session.user_token[-1] == Logic.Session.ConfirmPasswordFinalCharacter:
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
                if not Logic.User.__checkDataIntegrity(json):
                    raise ValueError("Invalid User data")

                newUser = Data.User(json = json, cript = True)
                newUser.registration_state = Logic.Session.generateEmailCode(newUser.email)
                newUser.insert()

                subject = "Subject: Confirm your CodeDefender's account\n\n"
                payload = "Login and type the following code to complete your registration : "
                Logic.Email.sendEmail(newUser.email, subject, payload, newUser.registration_state)

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
                loggedUser = Data.User(json = json, cript = True).search()[0]
                token = Logic.Session.generateLoginToken(loggedUser.email, loggedUser.registration_state)

                if (len(loggedUser.registration_state) > 1 and
                    loggedUser.registration_state[-1] == Logic.Session.RecoverAccountFinalCharacter):
                    raise ConnectionRefusedError('Could not login because the user have asked for recovery account')

                session = Data.Session(user_token = token, id_user = loggedUser.id)
                session.insert()

                redirectSettings = Data.Redirect.getSettings()

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

        def logOut(token: str) -> JSONResponse:
            try:
                session = Data.Session(user_token = token)
                session.delete()

                redirectPage = Data.Redirect.getSettings()['notLoggedRedirect']
                res = JSONResponse(content={"MSG": "Success", 'REDIRECT': redirectPage})
                res.delete_cookie(key='TOKEN', samesite='none', secure=True)
                return res
            except exc.InvalidRequestError:
                res = JSONResponse({'MSG': "Could not delete the session"})
                return res

        def confirmEmail(json : dict, token : str) -> JSONResponse:
            try:
                session = Data.Session(user_token = token).search()[0]

                user = Data.User(id = session.id_user, cript = True).search()[0]

                if(json['CODE'] != user.registration_state) :
                    raise IndexError("Invalid Code!")

                user.update(REGISTRATION_STATE = "")
                session.delete()

                session = Data.Session(user_token = Logic.Session.generateLoginToken(user.email, ""), id_user = user.id)
                session.insert()

                redirectPage = Data.Redirect.getSettings()['LoggedRedirect']
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
                user = Data.User(json)
                user = user.search()[0]

                code = Logic.Session.generateNewPasswordCode(user.email)
                user.update(REGISTRATION_STATE = code)

                subject = "Subject: Recover your CodeDefenders' Account\n\n"
                payload = "Here it is the code you need to set a new password: "
                Logic.Email.sendEmail(user.email, subject, payload, code)
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
                user = Data.User(registration_state = json['CODE'], cript = True)
                user = user.search()[0]
                user.update(PW = json['PW'], REGISTRATION_STATE = "")
                redirectPage = Data.Redirect.getSettings()['notLoggedRedirect']
                res = JSONResponse(content={"MSG": "Success", 'REDIRECT': redirectPage})
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
                session = Data.Session(user_token = token).search()[0]
                user = Data.User(id = session.id_user, cript = True).search()[0]
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
            return Data.Session.generateToken(email, time.ctime())[0:len] + Logic.Session.ConfirmPasswordFinalCharacter

        def generateNewPasswordCode(email: str, len=10) -> str:
            return Data.Session.generateToken(email, time.ctime())[0:len] + Logic.Session.RecoverAccountFinalCharacter

        def generateLoginToken(email: str, registrationState: str):
            while True:
                token = Data.Session.generateToken(email, time.ctime())

                if len(registrationState) > 0:
                    token = token + Logic.Session.ConfirmPasswordFinalCharacter
                else:
                    token = token + Logic.Session.LoggedUserFinalCharacter

                if len(Data.Session(user_token = token).search()) == 0:
                    break
            return token

    class Email:
        username = None
        password = None
        STMPServer = None
        port = None

        def sendEmail(addressee: str, subject : str, payload : str, token: str):
            if Logic.Email.username is None or\
                Logic.Email.password is None or\
                Logic.Email.STMPServer is None or\
                Logic.Email.port is None:
                Logic.Email.__initEmailSettings__()

            try:
                msg = subject + payload + token
                email = smtplib.SMTP(Logic.Email.STMPServer, Logic.Email.port)
                email.ehlo()
                email.starttls()
                email.login(Logic.Email.username, Logic.Email.password)
                email.sendmail(Logic.Email.username,addressee, msg.encode('utf-8'))
                email.quit()
            except:
                raise smtplib.SMTPException('Could not send email')

        def __initEmailSettings__():
            config = configparser.ConfigParser()
            config.read('settings/utils.ini')
            #password = "progettosad6!"
            Logic.Email.username = config['EmailSettings']['username']
            Logic.Email.password = config['EmailSettings']['password']
            Logic.Email.STMPServer = config['EmailSettings']['STMPServer']
            Logic.Email.port = config['EmailSettings']['port']
