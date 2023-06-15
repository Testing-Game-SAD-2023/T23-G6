class View {

    constructor(model) {
        model.redirect();
        this.model = model;
        this.model.on("modelRedirect", this.redirect.bind(this))
        this.model.on("modelShowAlert", this.showAlert.bind(this))

        this.htmlTag = document.getElementById("htmlTag");
    }

    showAlert({msg}){
        alert(msg);
    }

    on(event, callback) {
        this[event] = callback;
    }

    emit(event, data) {
        if (typeof this[event] === 'function')
          this[event](data);
    }

    redirect({ page }) {
        if (page == location.pathname.split("/").slice(-1).toString())
            this.htmlTag.hidden = false;
          else
            window.location.href = page;
    }

}