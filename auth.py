

import hashlib
import re

import storage

MAX_FAILED_ATTEMPTS = 3



def _hash_password(password: str) -> str:
   
    return hashlib.sha256(password.encode()).hexdigest()


def _check_password(input_password: str, stored_hash: str) -> bool:
    
    return _hash_password(input_password) == stored_hash




def _validate_username(username: str) -> str | None:
    
    if len(username) < 3:
        return "Логин должен содержать не менее 3 символов."
    if not re.fullmatch(r"[A-Za-z0-9]+", username):
        return "Логин может содержать только латинские буквы и цифры."
    return None


def _validate_password(password: str) -> str | None:
   
    if len(password) < 6:
        return "Пароль должен содержать не менее 6 символов."
    return None



def register() -> None:
   
    print("\n─── Регистрация ───")
    username = input("Логин: ").strip()

    error = _validate_username(username)
    if error:
        print(f"[Ошибка] {error}")
        return

    users = storage.load_users()
    if username in users:
        print(f"[Ошибка] Пользователь «{username}» уже существует.")
        return

    password = input("Пароль: ").strip()
    error = _validate_password(password)
    if error:
        print(f"[Ошибка] {error}")
        return

    users[username] = {
        "password_hash": _hash_password(password),
        "balance": 0.0,
        "blocked": False,
        "failed_attempts": 0,
    }
    storage.save_users(users)
    print(f"[OK] Пользователь «{username}» успешно зарегистрирован.")




def login() -> str | None:
    
    print("\n─── Вход в систему ───")
    username = input("Логин: ").strip()
    users = storage.load_users()

    if username not in users:
        print("[Ошибка] Пользователь не найден.")
        return None

    user = users[username]

    if user["blocked"]:
        print("[Ошибка] Аккаунт заблокирован из-за превышения числа неудачных попыток входа.")
        return None

    password = input("Пароль: ").strip()

    if _check_password(password, user["password_hash"]):
        
        user["failed_attempts"] = 0
        storage.save_users(users)
        print(f"[OK] Добро пожаловать, {username}!")
        return username
    else:
       
        user["failed_attempts"] += 1
        remaining = MAX_FAILED_ATTEMPTS - user["failed_attempts"]

        if remaining <= 0:
            user["blocked"] = True
            storage.save_users(users)
            print("[Ошибка] Неверный пароль. Аккаунт заблокирован.")
        else:
            storage.save_users(users)
            print(f"[Ошибка] Неверный пароль. Осталось попыток: {remaining}.")

        return None
