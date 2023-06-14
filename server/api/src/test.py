import unittest
from view import View
from model import Model
from fastapi.responses import JSONResponse
from parameterized import parameterized

class Test(unittest.TestCase):
    
    def setUp(self):
        json={}
        json["NAME"]="Fabio"
        json["SURNAME"]="Verdi"
        json["EMAIL"]="fabio.test@test.test"
        json["DEGREE"]="Degree"
        json["PW"]="test12345"
        json["REGISTRATION_STATE"]="123"
        self.NewUser = Model.User(json)
        self.NewUser.insert()
    
    @parameterized.expand([
        #   TEST - CAMPI VUOTI
        ["Empty","","","","",""],   
        #   TEST - NOME NON VALIDO                                            
        ["InvalidName", "34", "Rossi","mario.rossi@gmail.com","Degree","mariorossi34"],
        #   TEST - SURNAME NON VALIDO
        ["InvalidSurname", "Mario", "34","mario.rossi@gmail.com","Degree","mariorossi34"],
        #   TEST - EMAIL NON VALIDA
        ["InvalidEmail", "Mario", "Rossi","mario.com","Degree","mariorossi34"],
        #   TEST - PASSWORD TROPPO LUNGA
        ["PasswordTooLong","Mario", "Rossi","mario.rossi@gmail.com","Degree","mariorossi345678910111213141516171819"]
    ])
    def testRegistrazioneCampiNonValidi(self,testname,name,surname,email,degree,password):
        json={}
        json["NAME"]=name
        json["SURNAME"]=surname
        json["EMAIL"]=email
        json["DEGREE"]=degree
        json["PW"]=password
        self.assertEqual(View.RegistraGiocatore(json).body,JSONResponse({'MSG': "Invalid User data"}).body)
    
    @parameterized.expand([
        #TEST - UTENTE GIA REGISTRATO
        ["AlreadyRegistered","Fabio","Verdi","fabio.test@test.test","Degree","test12345"]
    ]) 
    def testRegistrazioneUtenteGiaRegistrato(self,testname,name,surname,email,degree,password):
        json={}
        json["NAME"]=name
        json["SURNAME"]=surname
        json["EMAIL"]=email
        json["DEGREE"]=degree
        json["PW"]=password
        self.assertEqual(View.RegistraGiocatore(json).body,JSONResponse({'MSG': "Invalid request"}).body)
    
    @parameterized.expand([
        #   TEST - UTENTE NON REGISTRATO
        ["NotRegistered","test@test.test","test12345"],
        #   TEST - UTENTE REGISTRATO CON CREDENZIALE SBAGLIATA
        ["RegisteredWrongCredential","fabio.test@test.test","test54321"],
    ])
    def testLogin(self,testname,email,password):
        json={}
        json["EMAIL"]=email
        json["PW"]=password
        self.assertEqual(View.LoginGiocatore(json).body,JSONResponse({'MSG': "Invalid credentials"}).body)

    @parameterized.expand([
        #   TEST - UTENTE NON REGISTRATO
        ["NotRegistered","test@test.test"],
    ])    
    def testPasswordResetSendEmail(self,testname,email):
        json={}
        json["EMAIL"]=email
        self.assertEqual(View.RecuperaAccountInviaEmail(json).body,JSONResponse({'MSG': "Unregistered email"}).body)
    
    @parameterized.expand([
        #   TEST - CODICE ERRATO
        ["NotRegistered","fabio.test@test.test","0000"],
    ])    
    def testPasswordResetPassword(self,testname,email,code):
        json={}
        json["EMAIL"]=email
        json['CODE']=code
        self.assertEqual(View.RecuperaAccountCambiaPassword(json).body,JSONResponse({'MSG': "The code is invalid"}).body)
    
    
    def tearDown(self):
        self.NewUser.delete()

if __name__ == "__main__":
    unittest.main()
