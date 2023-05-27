class View {

    showAlert(message){
        alert(message);
    }

    on(event, callback) {
        this[event] = callback;
    }
    
    emit(event, data) {
        if (typeof this[event] === 'function') 
          this[event](data);
    }
    
}