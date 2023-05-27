class homeView extends View {
    constructor() {
        super();
        this.logoutButton = document.getElementById("logoutButton")
        this.logoutButton.addEventListener("click", this.handleLogout.bind(this))
    }

    handleLogout(event) {
        event.preventDefault();
        this.emit('logout', {});
    }

}