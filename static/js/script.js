function showAlert(message) {
    let alertBox = document.createElement('div');
    alertBox.className = `alert`
    alertBox.innerText = message;

    document.body.appendChild(alertBox);

    setTimeout(() => {
        alertBox.remove();
    }, 3000); // Remove após 3 segundos
}