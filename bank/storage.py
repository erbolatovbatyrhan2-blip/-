

import json
import os

USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")
TRANSACTIONS_DIR = os.path.join(os.path.dirname(__file__), "transactions")


def _ensure_transactions_dir() -> None:
    os.makedirs(TRANSACTIONS_DIR, exist_ok=True)


def load_users() -> dict:
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(users: dict) -> None:
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)



def load_transactions(username: str) -> list:

    _ensure_transactions_dir()
    path = os.path.join(TRANSACTIONS_DIR, f"{username}.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def append_transaction(username: str, transaction: dict) -> None:
   
    _ensure_transactions_dir()
    transactions = load_transactions(username)
    transactions.append(transaction)
    path = os.path.join(TRANSACTIONS_DIR, f"{username}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(transactions, f, ensure_ascii=False, indent=2)
        
