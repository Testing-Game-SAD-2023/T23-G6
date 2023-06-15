baseURL = 'http://127.0.0.1/api/'
class Model{

    constructor(){}

    emit(event, data) {
        if (typeof this[event] === 'function')
          this[event](data);
    }

    on(event, callback) {
        this[event] = callback;
    }

    passwordRecoveryChangePassword(code, password) {

      let requestBody = new Object();
      requestBody.CODE = code
      requestBody.PW = password

      let jsonString = JSON.stringify(requestBody);

      fetch(baseURL+'RecuperaAccountCambiaPassword', {
          method: 'POST',
          withCredentials: true,
          headers: {
            "Access-Control-Allow-Origin": "http://127.0.0.1:1200",
            'Content-Type': 'application/json'
          },
          credentials: 'include',
          body: jsonString
        })
          .then(response => response.json())
          .then(response => {
            if(response['MSG'] !== 'Success')
              throw new Error(response['MSG'])
            else {
              this.emit('modelShowAlert', {msg : "Password changed successfully!"})
              this.emit('modelRedirect', {page : response['REDIRECT']})
            }})
          .catch(error => {
            console.log(error)
            this.emit('modelShowAlert', {msg : "Something went wrong... Check your code or passwords!"})})

    }

    passwordRecoverySendEmail(email){

      let requestBody = new Object();
      requestBody.EMAIL = email;

      let jsonString = JSON.stringify(requestBody);

      fetch(baseURL+'RecuperaAccountInviaEmail', {
          method: 'POST',
          withCredentials: true,
          headers: {
            "Access-Control-Allow-Origin": "http://127.0.0.1:1200",
            'Content-Type': 'application/json'
          },
          credentials: 'include',
          body: jsonString
        })
          .then(response => response.json())
          .then(response => {
            if(response['MSG'] !== 'Success')
              throw new Error(response['MSG'])
            else
              this.emit('modelShowPageNewPassword', {})})
          .catch(error => {
            console.log(error)
            this.emit('modelShowAlert', {msg : "Invalid email!"})})
    }

    logout(){

      fetch(baseURL+'LogOut', {
        method: 'POST',
        withCredentials: true,
        headers: {
          "Access-Control-Allow-Origin": "http://127.0.0.1:1200",
          'Content-Type': 'application/json'
        },
        credentials: 'include'
      })
        .then(response => response.json())
        .then(response => {
          if(response['MSG'] !== 'Success')
            throw new Error(response['MSG'])
          else
            this.emit('modelRedirect', {page : response['REDIRECT']})})
        .catch(error => {
          console.log(error)
          this.emit('modelShowAlert', {msg : "Logout failed!"})})
    }

    ConfermaEmail(secretCode) {
      let requestBody = new Object();
      requestBody.CODE = secretCode;

      let jsonString = JSON.stringify(requestBody);

      fetch(baseURL+'ConfermaEmail', {
        method: 'POST',
        withCredentials: true,
        headers: {
          "Access-Control-Allow-Origin": "http://127.0.0.1:1200",
          'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: jsonString
      })
        .then(response => response.json())
        .then(response => {
          if(response['MSG'] !== 'Success')
            throw new Error(response['MSG'])
          else
            this.emit('modelRedirect', {page : response['REDIRECT']})})
        .catch(error => {
          console.log(error)
          this.emit('modelShowAlert', {msg : "Invalid Code!"})})
    }

    RegistraGiocatore(name, surname, email, degree, password){

          var user = new Object()
          user.NAME = name
          user.SURNAME = surname
          user.EMAIL = email
          user.DEGREE = degree
          user.PW = password

          fetch(baseURL+'RegistraGiocatore', {
              method: 'POST',
              body: JSON.stringify(user)
          })
          .then(response => response.json())
          .then(response => {
            if(response['MSG'] !== 'Success')
                throw new Error(response['MSG'])
            else
                this.emit('modelShowAlert', {msg : 'Registration success!'});})
          .catch(error => {
            console.log(error)
            this.emit('modelShowAlert', {msg : 'Registration failed!'})})
    }

    LoginGiocatore(email, password){
        var user = new Object()
        user.EMAIL = email
        user.PW = password

        fetch(baseURL+'LoginGiocatore', {
            method: 'POST',
            body: JSON.stringify(user)
        })
        .then(response => response.json())
        .then(response => {
            if(response['MSG']!== 'Success')
                throw new Error(response['MSG'])
            else
                this.emit('modelRedirect', {page : response['REDIRECT']});
        })
        .catch(error => {
            console.log(error)
            this.emit('modelShowAlert', {msg : "Login failed!"})})
    }

    redirect(){
        let requestBody = new Object();
        requestBody.LOC = location.pathname.split("/").slice(-1).toString()

        fetch(baseURL+'Redirect', {
          method: 'POST',
          withCredentials: true,
          headers: {
            "Access-Control-Allow-Origin": "http://127.0.0.1:1200",
            'Content-Type': 'application/json'
          },
          credentials: 'include',
          body: JSON.stringify(requestBody)
        })
          .then(response => response.json())
          .then(response => {
            if(response['MSG']!== 'Success')
              throw new Error(response['MSG'])
            else
              this.emit('modelRedirect', {page : response['REDIRECT']});
          })
          .catch(() => this.emit('modelShowAlert', {msg : "Inavlid request"}))
    }

    OttieniDatiUtente(){
      fetch(baseURL+'OttieniDatiUtente', {
        method: 'POST',
        withCredentials: true,
        headers: {
          "Access-Control-Allow-Origin": "http://127.0.0.1:1200",
          'Content-Type': 'application/json'
        },
        credentials: 'include'
      })
        .then(response => response.json())
        .then(response => {
          if(response['MSG']!== 'Success')
            throw new Error(response['MSG'])
          else
            this.emit('modelWriteWelcomeMessage', {name : response['name'], surname : response['surname']});
        })
        .catch(() => { this.emit('modelWriteWelcomeMessage', {name : '???', surname : '???'});})
    }
}
