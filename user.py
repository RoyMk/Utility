import subprocess
from operator import index

import utils
from contextlib import redirect_stdout

from utils import admin_group


# macOS
# user creation command
# sysadminctl

# command
# sudo sysadminctl -addUser newusername -fullName "New User Full Name" -password newpassword


class User:
    def __init__(self,username,fullname,password):
        self.username = username
        self.fullname = fullname
        self.password = password
        self._private_create_user()


    def give_administrator_role(self):
        try:
            admin = [
                "sudo", "-S", "dscl",
                ".", "-append",
                "/Groups/admin",
                "GroupMembership", self.username
            ]
            self.execute_command(admin)
        except Exception as e:
            print("Could not run command")


    def delete_user(self):
        delete = [
            "sudo","dscl",
            ".", "-delete",
            f"/Users/{self.username}",

        ]
        self.execute_command(delete)
        # sudo dscl . -delete /Users/username


    def demote_administrator(self):
        try:
            demote = [
                "sudo", "-S", "dscl",
                ".", "-delete",
                "/Groups/admin",
                "GroupMembership", self.username
            ]


            self.execute_command(demote)
            print(f"Successfully Removed {self.username} to Standard User")

        except subprocess.SubprocessError as e:
            print(e)


    def check_user_exist(self):
        result = utils.admin_group()
        print(result)
        return result




    def is_user_admin(self):
        utils.admin_group(user = self.username)




    def execute_command(self,command):
        try:
            sub = subprocess.run(command,check=True,capture_output=True,text=True)
            print("Executed Creation Command")
        except Exception as e:
            print(e)

    # should not be called, internally this is called at instantiation
    def _private_create_user(self):
        try:
            if self.username not in self.check_user_exist():
                command = [
                    "sudo", "-S", "sysadminctl",
                    "-addUser", self.username,
                    "-fullName", self.fullname,
                    "-password", self.password
                ]
                print("password")
                self.execute_command(command)

            else:
                print("User already exists")
        except Exception as e:
            print(e)






if __name__ == "__main__":
    testUser = User("TestUser", "TestUserFullName", "Test")

