class homeView extends View {
    constructor(model) {
        super(model);

        this.model.on("modelWriteWelcomeMessage", this.WriteWelcomeMessage.bind(this))
        
        this.logoutButton = document.getElementById("logoutButton")
        this.WelcomeMessage = document.getElementById("WelcomeMessage")
        this.logoutButton.addEventListener("click", this.handleLogout.bind(this))

        this.model.OttieniDatiUtente()
    }

    handleLogout(event) {
        event.preventDefault();
        this.emit('logout', {});
    }

    WriteWelcomeMessage({ name, surname }){
        this.WelcomeMessage.innerHTML = name + ' ' + surname
    }

}