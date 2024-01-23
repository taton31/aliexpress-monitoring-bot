import json

def get_admins() -> set:
    with open('db/admins.txt', 'r', encoding='utf-8') as f:
        return eval(f.read())
    
def save_admins(ls: set):
    with open('db/admins.txt', 'w', encoding='utf-8') as f:
        f.write(str(ls))


def get_request_users() -> dict:
    with open('db/request_users.txt', 'r', encoding='utf-8') as f:
        return eval(f.read())
    
def save_request_users(ls: dict):
    with open('db/request_users.txt', 'w', encoding='utf-8') as f:
        f.write(str(ls))


def get_users() -> dict:
    with open('db/users.txt', 'r', encoding='utf-8') as f:
        return json.load(f)
    
def save_users(d: dict):
    with open('db/users.txt', 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False)