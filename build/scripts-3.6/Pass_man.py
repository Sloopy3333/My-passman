import sqlite3
from typing import Text
from cmd2 import Cmd
from sys import stdout, stderr
from getpass import getpass
from scripts.hash import hash
from scripts.Authhandler import AuthHandler
import pandas as pd
from scripts.AES256 import AESCipher
from tabulate import tabulate
import pyfiglet

tablefmt = "grid"
banner = pyfiglet.figlet_format("Pass-man")


class Pass_Man(Cmd):
    prompt = "passman> "
    intro = f"{banner}\nWelcome to Pypass press ? to list commands press ctrl+d to exit"

    # add new user
    def do_add_user(self, inp):
        """Add a new user to Pass-man"""
        stdout.write(
            "add a user name and master password press [y] to continue [n] to exit\n"
        )
        choice = input()
        if choice == "y":
            stdout.write(str("Enter your user name : "))
            user_name = input()
            enc_user_name = hash(user_name)
            master_pass = getpass()
            enc_mast_pass = hash(master_pass)
            connection = sqlite3.connect("bin//passman.db")
            cursor = connection.cursor()
            try:
                cursor.execute(
                    f"""CREATE TABLE {user_name}(
                                                        service text,
                                                        username text,
                                                        password text
                                                        )"""
                )
                cursor.execute(
                    f"INSERT INTO {user_name} VALUES (:service,:username,:password)",
                    {
                        "service": "passman",
                        "username": enc_user_name,
                        "password": enc_mast_pass,
                    },
                )
                connection.commit()
                stdout.write(f"sucessfuly created user {user_name}\n")

                connection.close()
            except:
                stderr.write(f"user {user_name} alredy exists\n")
        else:
            stdout.write("exit\n")

    # add new password
    def do_add_pass(self, inp):
        """add new service to existing user"""
        stdout.write(str("Enter your user name : "))
        user_name = input()
        master_pass = getpass()
        auth = AuthHandler()
        crediential, connection, cursor = auth.login(user_name, master_pass)
        while crediential:
            aes = AESCipher(master_pass)
            stdout.write("enter service name : ")
            service = input()
            stdout.write(f"enter user name for {service} : ")
            username = input()
            password = getpass()
            cursor.execute(
                f"INSERT INTO {user_name} VALUES (:service,:username,:password)",
                {
                    "service": service,
                    "username": aes.encrypt(username),
                    "password": aes.encrypt(password),
                },
            )
            connection.commit()
            stdout.write(f"sucessfuly added {service} to your passwords\n")
            stdout.write("press [y] to add another service or press[o] to exit\n")
            wish = input()
            if wish == "y":
                crediential = True
            else:
                crediential = False

    def do_list_users(self, inp):
        """List all user in pypass"""
        connection = sqlite3.connect("Pypass.db")
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        users = cursor.fetchall()
        stdout.write("Available users\n")
        print(tabulate(users, tablefmt=tablefmt))
        connection.close()

    def do_list_services(self, inp):
        """List services names for all passwords added by user"""
        stdout.write(str("Enter your user name : "))
        user_name = input()
        master_pass = getpass()
        auth = AuthHandler()
        crediential, connection, cursor = auth.login(user_name, master_pass)
        while crediential:
            cursor.execute(f"SELECT service FROM {user_name}")
            services = cursor.fetchall()
            stdout.write(f"Available services for {user_name}\n")
            print(tabulate(services, tablefmt=tablefmt))
            crediential = False

    def do_get_all(self, inp):
        """List all stored usernames and password of a user"""
        stdout.write(
            "this method will display all your password and username press [y] to continue [n] to quit\n"
        )
        wish = input()
        if wish == "y":
            stdout.write(str("Enter your user name : "))
            user_name = input()
            master_pass = getpass()
            auth = AuthHandler()
            crediential, connection, cursor = auth.login(user_name, master_pass)
            while crediential:
                cursor.execute(f"SELECT service,username,password FROM {user_name}")
                aes = AESCipher(master_pass)
                df = pd.DataFrame(
                    cursor.fetchall()[1:], columns=["services", "username", "password"]
                )
                connection.close
                for col in df.columns[1:]:
                    df[col] = df[col].apply(lambda x: aes.decrypt(x))
                print(
                    tabulate(
                        df,
                        headers=["services", "username", "password"],
                        tablefmt=tablefmt,
                    )
                )
                connection.close()
                crediential = False
        else:
            stdout.write("loged out\n")

    def do_get_pass(self, inp):
        """Get username and password for a given service example get_pass <service name>"""
        stdout.write(
            "this method will display your password and username without any encryption press [y] to continue [n] to quit\n"
        )
        wish = input()
        if wish == "y":
            stdout.write(str("Enter your user name : "))
            user_name = input()
            master_pass = getpass()
            auth = AuthHandler()
            crediential, connection, cursor = auth.login(user_name, master_pass)
            while crediential:
                service = inp
                aes = AESCipher(master_pass)
                cursor.execute(f"SELECT service,username,password FROM {user_name}")
                df = pd.DataFrame(
                    cursor.fetchall()[1:], columns=["services", "username", "password"]
                )
                df = df.loc[df["services"] == service]
                df["username"] = df["username"].apply(lambda x: aes.decrypt(x))
                df["password"] = df["password"].apply(lambda x: aes.decrypt(x))
                print(
                    tabulate(
                        df,
                        headers=["services", "username", "password"],
                        tablefmt=tablefmt,
                    )
                )
                crediential = False
                connection.close()
        else:
            stdout.write("loged out\n")

    def do_del_pass(self, inp):
        """delete password of a service example : del_pass <service name>"""
        stdout.write(str("Enter your user name : "))
        user_name = input()
        master_pass = getpass()
        stdout.write("enter service name :")
        inp = str(input())
        auth = AuthHandler()
        crediential, connection, cursor = auth.login(user_name, master_pass)
        while crediential:
            aes = AESCipher(master_pass)
            try:
                cursor.execute(f"DELETE FROM {user_name} WHERE service = '{inp}'")
                stdout.write(f"sucessfuly deleted {inp} from your passwords\n")
                stdout.write(
                    "press [y] to delete another service or press[o] to exit\n"
                )
                wish = input()
                if wish == "y":
                    crediential = True
                else:
                    crediential = False
                    connection.close()
            except:
                stderr.write(f"No service named {inp} exists")
                crediential = False

    def do_del_user(self, inp):
        """delete user from Pass-man"""
        stdout.write(str("Enter your user name : "))
        user_name = input()
        master_pass = getpass()
        auth = AuthHandler()
        crediential, connection, cursor = auth.login(user_name, master_pass)
        while crediential:
            aes = AESCipher(master_pass)
            try:
                cursor.execute(f"DROP TABLE {user_name}")
                stdout.write(f"sucessfuly deleted {user_name} from Pypass\n")
                stdout.write("press [y] to delete another user or press[o] to exit\n")
                wish = input()
                if wish == "y":
                    crediential = True
                else:
                    crediential = False
                    connection.close()
            except:
                stderr.write(f"No user named {user_name} exists")
                crediential = False

    def do_where(self, inp):
        """return loction of database"""
        stdout.write(f"{__file__[0:-20]}/bin\n")


def main():
    app = Pass_Man()
    app.cmdloop()


if __name__ == "__main__":
    main()

