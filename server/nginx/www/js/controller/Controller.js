class Controller{

    constructor(model, view){
        this.model = model;
        this.view = view;
        this.redirect()
        this.view.on('register', this.registerUser.bind(this));
        this.view.on('login', this.loginUser.bind(this));
        this.view.on('confirmEmail', this.confirmEmail.bind(this));
        this.view.on('logout', this.logout.bind(this));
        this.view.on('passwordRecoverySendEmail', this.passwordRecoverySendEmail.bind(this));
        this.view.on('passwordRecoveryChangePassword', this.passwordRecoveryChangePassword.bind(this));
        this.view.on('WelcomeMessage', this.WriteWelcomeMessage.bind(this));
    }
  

    passwordRecoveryChangePassword({ code, password1, password2 })
      {
        if (password1 !== password2)
          this.view.showAlert("Passwords don't match!")
        else
          this.model.passwordRecoveryChangePassword(code, password1, password2)
          .then(() => { this.view.showAlert("Password changed successfully!")
                        window.location.href = "/";})
          .catch(() => this.view.showAlert("Something went wrong... Check your code or passwords!"))
      }

    passwordRecoverySendEmail({email1, email2})
      {
        const validateEmail1 =  String(email1).toLowerCase().match(/\b[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,6}\b/g)
        if (validateEmail1 == null || email1 != email2)
          this.view.showAlert("Invalid email")
        else
          this.model.passwordRecoverySendEmail(email1)
          .then(() => this.view.showPageNewPassword())
          .catch(() => this.view.showAlert("Something went wrong... Check your emails!"))
      }

    logout()
    {

      this.model.logout()
          .then(response => location.href = response['REDIRECT'])
          .catch(() => this.view.showAlert("Logout failed!"))

    }

    confirmEmail({secretCode})
    {

      this.model.ConfermaEmail(secretCode)
          .then(response => location.href = response['REDIRECT'])
          .catch(() => this.view.showAlert("Wrong code!"))

    }

    registerUser({email, password, password2, name, surname, degree, check})
    {
        const validateEmail =  String(email).toLowerCase().match(/\b[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,6}\b/g)
        const validateName = String(name).toLowerCase().match(/^[A-Za-zèùàòé][a-zA-Z'èùàòé ]*$/g)
        const validateSurname = String(surname).toLowerCase().match(/^[A-Za-zèùàòé][a-zA-Z'èùàòé ]*$/g)

        if (check == false)
            this.view.showAlert("Please agree to the terms")

          else if (validateEmail == null)
            this.view.showAlert("Invalid email")

          else if (password < 7  || password > 32 )
            this.view.showAlert("Invalid password size")

          else if (password != password2)
            this.view.showAlert("Passwords do not match")

          else if (validateName == null)
            this.view.showAlert("Invalid Name")

          else if (validateSurname == null)
            this.view.showAlert("Invalid Surname")

          else
                this.model.RegistraGiocatore(name, surname, email, degree, password)
                .then(() => this.view.showAlert("Registration successful!"))
                .catch(() => this.view.showAlert("Registration failed!"))

          }

      loginUser({email, password})
      {
        const validateEmail =  String(email).toLowerCase().match(/\b[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,6}\b/g)
        if (validateEmail == null)
          this.view.showAlert("Invalid email")
        else
          this.model.LoginGiocatore(email, password)
          .then(response => location.href = response['REDIRECT'])
          .catch(() => this.view.showAlert("Login failed!"))
      }

      redirect(){
        this.model.redirect()
        .then(response => {
          if (response['REDIRECT'] == location.pathname.split("/").slice(-1).toString())
            document.getElementById("htmlTag").hidden = false;
          else
             location.href = response['REDIRECT']
          })
        .catch(error => {console.log(error);this.view.showAlert('Invalid request!')})
      }

      WriteWelcomeMessage(){
        console.log('WriteWelcomeMessage')
        this.model.OttieniDatiUtente()
        .then(response => document.getElementById('WelcomeMessage').innerHTML = response['name'] + ' ' + response['surname'] )
        .catch(error => {console.log(error);this.view.showAlert('Invalid request!')})
      }
}
