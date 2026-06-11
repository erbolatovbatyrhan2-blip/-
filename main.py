

import sys
import os


sys.path.insert(0, os.path.dirname(__file__))

import auth
import account
import report

def main_menu() -> None:
   
    while True:
        print("\n=== Консольный банк ===")
        print("1. Войти")
        print("2. Зарегистрироваться")
        print("0. Выход")

        choice = input("Выберите пункт: ").strip()

        if choice == "1":
            username = auth.login()
            if username:
                account_menu(username)

        elif choice == "2":
            auth.register()

        elif choice == "0":
            print("До свидания!")
            sys.exit(0)

        else:
            print("[Ошибка] Неизвестный пункт меню. Попробуйте ещё раз.")



def account_menu(username: str) -> None:
       while True:
        print(f"\n=== Меню аккаунта [{username}] ===")
        print("1. Пополнить счёт")
        print("2. Снять средства")
        print("3. Перевести другому пользователю")
        print("4. Отчёт (баланс и история)")
        print("0. Выйти из аккаунта")

        choice = input("Выберите пункт: ").strip()

        if choice == "1":
            account.deposit(username)

        elif choice == "2":
            account.withdraw(username)

        elif choice == "3":
            account.transfer(username)

        elif choice == "4":
            report.show_report(username)

        elif choice == "0":
            print(f"Выход из аккаунта [{username}].")
            return  

        else:
            print("[Ошибка] Неизвестный пункт меню. Попробуйте ещё раз.")




if __name__ == "__main__":
    main_menu()
