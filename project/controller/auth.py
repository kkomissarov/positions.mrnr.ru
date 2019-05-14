from model.project import get_users, get_password_by_login, get_login_key_by_login
from flask import session


def check_auth():
    if 'login_key' in session:
        user_keys = [user['login_key'] for user in get_users()]

        if session['login_key'] in user_keys:
            return True

        else:
            return False

    else:
        return False

def validate_password(login, password):

    #Берем из базы все логины пользователей
    user_logins = [user['login'] for user in get_users()]

    #Если присланный логин есть в списке пользователей - проверяем корректность пароля
    if login in user_logins:
        if password == get_password_by_login(login):
            session['login_key'] = get_login_key_by_login(login)
            return True

        #Если пароль неправильный - false
        else:
            return False


    #Если логина нет среди логинов в базе - сразу отдаем false
    return False



if __name__ == '__main__':
    pass