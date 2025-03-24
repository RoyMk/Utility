import subprocess

def admin_group(user = None):
    admin_users = [
        "dscl", ".",
        "-read","/Groups/admin",
        "GroupMembership"
    ]

    sub = subprocess.run(admin_users, check=True, capture_output=True, text=True)
    if sub.returncode  == 0:

        return [user for user in sub.stdout.split(" ") if user in user]

    else:
        return sub.stderr



