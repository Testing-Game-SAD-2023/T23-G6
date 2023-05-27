
class Model{

    constructor(){}

    passwordRecoveryChangePassword(code, password) {

      let requestBody = new Object();
      requestBody.CODE = code
      requestBody.PW = password

      let jsonString = JSON.stringify(requestBody);

      return fetch('http://127.0.0.1/api/RecuperaAccountCambiaPassword', {
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
              throw new Error(response['MSG'])})
          .catch(error => {
            console.log(error)
            throw error})

    }

    passwordRecoverySendEmail(email){

      let requestBody = new Object();
      requestBody.EMAIL = email;

      let jsonString = JSON.stringify(requestBody);

      return fetch('http://127.0.0.1/api/RecuperaAccountInviaEmail', {
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
              throw new Error(response['MSG'])})
          .catch(error => {
            console.log(error)
            throw error})

    }

    logout(){

      return fetch('http://127.0.0.1/api/LogOut', {
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
            return response})
        .catch(error => {
          console.log(error)
          throw error})

    }

    ConfermaEmail(secretCode) {
      let requestBody = new Object();
      requestBody.CODE = secretCode;

      let jsonString = JSON.stringify(requestBody);

      return fetch('http://127.0.0.1/api/ConfermaEmail', {
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
            return response})
        .catch(error => {
          console.log(error)
          throw error})
    }

    RegistraGiocatore(name, surname, email, degree, password){

          var user = new Object()
          user.NAME = name
          user.SURNAME = surname
          user.EMAIL = email
          user.DEGREE = degree
          user.PW = password

          return fetch('http://127.0.0.1/api/RegistraGiocatore', {
              method: 'POST',
              body: JSON.stringify(user)
          })
          .then(response => response.json())
          .then(response => {
            if(response['MSG'] !== 'Success')
                throw new Error(response['MSG'])})
          .catch(error => {
            console.log(error)
            throw error})
    }

    LoginGiocatore(email, password){
        var user = new Object()
        user.EMAIL = email
        user.PW = password
        return fetch('http://127.0.0.1/api/LoginGiocatore', {
            method: 'POST',
            body: JSON.stringify(user)
        })
        .then(response => response.json())
        .then(response => {
            console.log(response)
            console.log(response.cookies)
            if(response['MSG']!== 'Success')
                throw new Error(response['MSG'])
            else
                return response})
        .catch(error => {
            console.log(error)
            throw error})
    }

    redirect(){
        let requestBody = new Object();
        requestBody.LOC = location.pathname.split("/").slice(-1).toString()

        return fetch('http://127.0.0.1/api/Redirect', {
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
              return response
          })
          .catch(error => { throw error})
    }
}
