

from datetime import datetime

import storage


def _now() -> str:

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _parse_amount(raw: str) -> float | None:
    """
    Преобразует строку в положительное число.
    Возвращает float или None, если строка некорректна.
    """
    try:
        amount = float(raw.strip().replace(",", "."))
    except ValueError:
        return None
    if amount <= 0:
        return None
    return amount


def _record(username: str, tx_type: str, amount: float, note: str = "") -> None:
   
    storage.append_transaction(username, {
        "type": tx_type,
        "amount": amount,
        "date": _now(),
        "note": note,
    })


def deposit(username: str) -> None:
   
    raw = input("Сумма пополнения: ").strip()
    amount = _parse_amount(raw)
    if amount is None:
        print("[Ошибка] Введите корректную положительную сумму.")
        return

    users = storage.load_users()
    users[username]["balance"] = round(users[username]["balance"] + amount, 2)
    storage.save_users(users)
    _record(username, "deposit", amount)

    print(f"[OK] Счёт пополнен на {amount:.2f}. Текущий баланс: {users[username]['balance']:.2f} ₸")



def withdraw(username: str) -> None:
  
    raw = input("Сумма снятия: ").strip()
    amount = _parse_amount(raw)
    if amount is None:
        print("[Ошибка] Введите корректную положительную сумму.")
        return

    users = storage.load_users()
    balance = users[username]["balance"]

    if amount > balance:
        print(f"[Ошибка] Недостаточно средств. Текущий баланс: {balance:.2f} ₸")
        return

    users[username]["balance"] = round(balance - amount, 2)
    storage.save_users(users)
    _record(username, "withdraw", amount)

    print(f"[OK] Снято {amount:.2f} ₸. Текущий баланс: {users[username]['balance']:.2f} ₸")




def transfer(username: str) -> None:
   
    recipient = input("Логин получателя: ").strip()

    if recipient == username:
        print("[Ошибка] Нельзя переводить средства самому себе.")
        return

    users = storage.load_users()

    if recipient not in users:
        print(f"[Ошибка] Пользователь «{recipient}» не найден в системе.")
        return

    raw = input("Сумма перевода: ").strip()
    amount = _parse_amount(raw)
    if amount is None:
        print("[Ошибка] Введите корректную положительную сумму.")
        return

    sender_balance = users[username]["balance"]
    if amount > sender_balance:
        print(f"[Ошибка] Недостаточно средств. Текущий баланс: {sender_balance:.2f} ₸")
        return


    users[username]["balance"] = round(sender_balance - amount, 2)
    users[recipient]["balance"] = round(users[recipient]["balance"] + amount, 2)
    storage.save_users(users)


    timestamp = _now()
    storage.append_transaction(username, {
        "type": "transfer_out",
        "amount": amount,
        "date": timestamp,
        "note": f"→ {recipient}",
    })
    storage.append_transaction(recipient, {
        "type": "transfer_in",
        "amount": amount,
        "date": timestamp,
        "note": f"← {username}",
    })

    print(
        f"[OK] Переведено {amount:.2f} ₸ пользователю «{recipient}». "
        f"Текущий баланс: {users[username]['balance']:.2f} ₸"
    )
