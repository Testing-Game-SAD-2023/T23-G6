class passwordRecoveryView extends View {
    constructor(model) {
        super(model)
        
        this.emailInput1 = document.getElementById("emailInput1")
        this.emailInput2 = document.getElementById("emailInput2")
        this.sendEmailButton = document.getElementById("sendEmailButton")
        this.sendEmailButton.addEventListener("click", this.handleSendEmail.bind(this))

        this.codeInput = document.getElementById("codeInput")
        this.passwordInput1 = document.getElementById("passwordInput1")
        this.passwordInput2 = document.getElementById("passwordInput2")
        this.ChangePasswordButton = document.getElementById("ChangePasswordButton")
        this.ChangePasswordButton.addEventListener("click", this.handleChangePassword.bind(this))

        this.model.on("modelShowPageNewPassword", this.showPageNewPassword.bind(this))
    }

    handleSendEmail(event) {
        event.preventDefault();
        const email1 = this.emailInput1.value
        const email2 = this.emailInput2.value

        this.emit('passwordRecoverySendEmail', { email1, email2 });
    }

    handleChangePassword(event) {
        event.preventDefault();
        const code = this.codeInput.value
        const password1 = this.passwordInput1.value
        const password2 = this.passwordInput2.value

        this.emit('passwordRecoveryChangePassword', { code, password1, password2 });
    }

    showPageNewPassword() {
        document.getElementById("divEmail1").hidden = true
        document.getElementById("divEmail2").hidden = true
        document.getElementById("sendEmailText").hidden = true
        document.getElementById("sendEmailButton").hidden = true

        document.getElementById("divpw1").hidden = false
        document.getElementById("divpw2").hidden = false
        document.getElementById("TypeCodeText").hidden = false
        document.getElementById("divCode").hidden = false
        document.getElementById("ChangePasswordButton").hidden = false
    }

}