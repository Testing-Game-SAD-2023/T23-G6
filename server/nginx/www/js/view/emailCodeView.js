class emailCodeView extends View {
    constructor(model) {
        super(model)
        this.secretCode = document.getElementById("secretCode")

        this.confirmButton = document.getElementById("confirmButton")
        this.confirmButton.addEventListener("click", this.handleConfirmCode.bind(this))

        this.logoutButton = document.getElementById("logoutButton")
        this.logoutButton.addEventListener("click", this.handleLogout.bind(this))
    }

    handleConfirmCode(event) {
        event.preventDefault();
        const secretCode = this.secretCode.value

        this.emit('confirmEmail', { secretCode });
    }

    handleLogout(event) {
        event.preventDefault();
        this.emit('logout', {});
    }

}