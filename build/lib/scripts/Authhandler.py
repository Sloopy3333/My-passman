import sqlite3
from scripts.hash import check
from sys import stdout


class AuthHandler:
    def login(self, user, mast_pass):
        connection = sqlite3.Connection("bin//passman.db")
        cursor = connection.cursor()
        try:
            cursor.execute(
                f"SELECT username, password from {user} WHERE service='passman'"
            )
        except Exception as e:
            stdout.write(str("User name or Password does not match"))
        cred = cursor.fetchone()
        if (check(user, cred[0])) & (check(mast_pass, cred[1])):
            return True, connection, cursor
        else:
            stdout.write(str("User name or Password does not match"))
            return False, None, None


test = AuthHandler()
print(test.login("user1", "user1"))

