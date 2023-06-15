class Controller{

    constructor(model, view){
        this.model = model;
        this.view = view;
        this.view.on('register', this.registerUser.bind(this));
        this.view.on('login', this.loginUser.bind(this));
        this.view.on('confirmEmail', this.confirmEmail.bind(this));
        this.view.on('logout', this.logout.bind(this));
        this.view.on('passwordRecoverySendEmail', this.passwordRecoverySendEmail.bind(this));
        this.view.on('passwordRecoveryChangePassword', this.passwordRecoveryChangePassword.bind(this));
    }

    passwordRecoveryChangePassword({ code, password1, password2 })
      {
        if (password1 !== password2)
          this.view.showAlert({msg : "Passwords don't match!"})
        else
          this.model.passwordRecoveryChangePassword(code, password1, password2)
      }

    passwordRecoverySendEmail({email1, email2})
      {
        const validateEmail1 =  String(email1).toLowerCase().match(/\b[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,6}\b/g)
        if (validateEmail1 == null || email1 != email2)
          this.view.showAlert({msg : "Invalid email"})
        else
          this.model.passwordRecoverySendEmail(email1)
      }

    logout()
    {
      this.model.logout()
    }

    confirmEmail({secretCode})
    {
      this.model.ConfermaEmail(secretCode)
    }

    registerUser({email, password, password2, name, surname, degree, check})
    {
        const validateEmail =  String(email).toLowerCase().match(/\b[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,6}\b/g)
        const validateName = String(name).toLowerCase().match(/^[A-Za-zèùàòé][a-zA-Z'èùàòé ]*$/g)
        const validateSurname = String(surname).toLowerCase().match(/^[A-Za-zèùàòé][a-zA-Z'èùàòé ]*$/g)

        if (check == false)
            this.view.showAlert({msg :"Please agree to the terms"})

          else if (validateEmail == null)
            this.view.showAlert({msg : "Invalid email"})

          else if (password < 7  || password > 32 )
            this.view.showAlert({msg : "Invalid password size"})

          else if (password != password2)
            this.view.showAlert({msg : "Passwords do not match"})

          else if (validateName == null)
            this.view.showAlert({msg : "Invalid Name"})

          else if (validateSurname == null)
            this.view.showAlert({msg : "Invalid Surname"})

          else
            this.model.RegistraGiocatore(name, surname, email, degree, password)

          }

      loginUser({email, password})
      {
        const validateEmail =  String(email).toLowerCase().match(/\b[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,6}\b/g)
        if (validateEmail == null)
          this.view.showAlert({msg : "Invalid email"})
        else
          this.model.LoginGiocatore(email, password)
      }

}
