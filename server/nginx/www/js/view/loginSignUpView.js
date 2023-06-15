class loginSignUpView extends View {
    constructor(model) {
        super(model)
        this.registerEmail = document.getElementById("registerEmail")
        this.registerPassword = document.getElementById("registerPassword")
        this.registerPassword2 = document.getElementById("registerRepeatPassword")
        this.registerName = document.getElementById("registerName")
        this.registerSurname = document.getElementById("registerSurname")
        this.registerDegree = document.getElementById("registerDegree")
        this.registerCheck = document.getElementById("registerCheck")

        this.loginEmail = document.getElementById("loginEmail")
        this.loginPassword = document.getElementById("loginPassword")

        this.registerButton = document.getElementById("registerButton")
        this.registerButton.addEventListener("click", this.handleRegistration.bind(this))

        this.loginButton = document.getElementById("loginButton")
        this.loginButton.addEventListener("click", this.handleLogin.bind(this))
    }

    handleRegistration(event) {
        event.preventDefault();
        const email = this.registerEmail.value
        const password = this.registerPassword.value
        const password2 = this.registerPassword2.value
        const name = this.registerName.value
        const surname = this.registerSurname.value
        const degree = this.registerDegree.value
        const check = this.registerCheck.checked

        this.emit('register', { email, password, password2, name, surname, degree, check});
    }

    handleLogin(event) {
        event.preventDefault();
        const email = this.loginEmail.value
        const password = this.loginPassword.value
        this.emit('login', { email, password});
    }

}
