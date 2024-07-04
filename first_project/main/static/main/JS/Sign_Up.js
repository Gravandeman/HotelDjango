function signUp() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('error-message');

    // Правильные значения для входа
    const correctUsername = 'Admin';
    const correctPassword = 'Admin';

    // Проверка введенных значений
    if (username === correctUsername && password === correctPassword) {
        // Перенаправление на страницу numbers.html
        window.location.href = '/';
    } else {
        // Показ сообщения об ошибке
        errorMessage.textContent = 'Неверное имя пользователя или пароль. Пожалуйста, попробуйте снова.';
    }
}
