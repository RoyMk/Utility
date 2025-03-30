import subprocess
from operator import index


class WinUser:
    def __init__(self, user_name = None,password = None,full_name =None,description = "None"):
        self.user_name = user_name
        self.password = password
        self.full_name = full_name
        self.description = description


    def create_account(self):
        account = [
            "powershell", "-Command",
            f"New-LocalUser -Name '{self.user_name}' "
            f"-Password (ConvertTo-SecureString '{self.password}' "
            f"-AsPlainText -Force) -FullName '{self.full_name}' "
            f"-Description '{self.description}'"
        ]

        self.execute(account)

    def delete_user(self, user_name):
        delete = [
            "net","user",f'{user_name}',
            "/delete"
        ]
        self.execute(delete)

    def list_users(self):
        get_users = [
            "net","user",
        ]
        output = self.execute(get_users)
        return output.stdout


    def user_exists(self, user_name = None, show_user_details = False):
        """   Check if a user exists in the users list.
              :param user_name: Users user name on the system.
              :param show_user_details: Whether or not to show extra details about the user.
              :return:
        """
        output = self.list_users().split(" ")
        trimmed_result = [x.replace("\n","").lower() for x in output if x.strip()]

        for result in trimmed_result:
            if user_name in result:
                if show_user_details:
                    return self.get_account_details(user_name).stdout
                return f"User {user_name} exists"
        return f"User {user_name} not found"


    def get_account_details(self,user_name):
        return self.execute(["net","user",f'{user_name}'])

    def execute(self,command):
        try:
            run = subprocess.run(command,check=True,capture_output=True,text=True)
            if run.returncode == 0:
                print(f"Successfully executed command {command}")
                return run
        except Exception as e:
            print(e)

    # ['makeuser', 'john', '123', 'john', 'an', 'account']
    def parse_user_commad(self,command):
        pass


print("Welcome to WinMan\n")
print("Enter Commands below, example: makeuser[username password fullname description]\nmakeuser,admin,123,Administrator,An account with admin rights")
print("Commands should be separated by a single comma")
user = WinUser()
while True:
    cinput = input("> ")
    # will be changed to spaces later
    usplit = cinput.split(",")
    match usplit[0]:
        case "makeuser":
            trimmed_result = [x.strip() for x in usplit if x.strip()]
            user.user_name = trimmed_result[1]
            user.password =  trimmed_result[2]
            user.full_name = trimmed_result[3]
            user.description = " ".join(trimmed_result[4])
            user.create_account()

        case "delete_user":
            user.delete_user(usplit[1])





    """
    ====== THE CODE BELOW WAS DEPRECATED ======
    This code was redundant, as the user should only need to type the values not the flags, the flags we already
    pre-set in the methods using subprocess call.
    
    cinput = input("> ")
    usplit = cinput.split(" ")
    
    get all values in array up to and including -d, then we concatenate the remaining values starting at -d but not including -d.
    concat_values = usplit[:usplit.index('-d') + 1] + [" ".join(usplit[usplit.index('-d') + 1:])]
    
    Begin at index 2 and step 2 indices per iteration until the end of the array. This grabs all the values
    and omits the command.
    commands = [concat_values[command] for command in range(2,len(concat_values),2)]
    
    """
    pass




