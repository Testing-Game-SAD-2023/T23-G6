class homeView extends View {
    constructor() {
        super();
        this.logoutButton = document.getElementById("logoutButton")
        this.WelcomeMessage = document.getElementById("WelcomeMessage")
        this.logoutButton.addEventListener("click", this.handleLogout.bind(this))
    }

    handleLogout(event) {
        event.preventDefault();
        this.emit('logout', {});
    }

    handleWelcomeMessage(){
        console.log('Welcome message');
        this.emit('WelcomeMessage', {});
    }
    
}