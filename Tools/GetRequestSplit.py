from http import client
from os import makedirs

print("NOTE: this script only provides basic request needs, headers and arguments, retries are not supported")

name = input("Enter name of folder to place split files into, leave blank for def=\"split\"\n:") or "split"
url = input("Enter pure host site url to perform a get request from ex=[raw.githubuser.com]\n:")
access = input("Enter pure access url to access '/split{n}.txt' from [/n1/n2/...], def='/'\n:")
conn_type = input("ConType: 'HTTPS'|'HTTP'\n:").upper()
amount = int(input("Enter fetch amount, must be an integer\n:"))

makedirs(name, exist_ok=True)
print("CREATED SPLIT FOLDER AT RELATIVE LOCATION", name)

for i in range(amount):
    print("REQUESTING", i)
    conn = client.HTTPSConnection(url) if conn_type == "HTTPS" else client.HTTPConnection(url)
    conn.request("GET", f"{access}/split{i}.txt")
    response = conn.getresponse()
    print("RESPONSE STATUS:", response.status, response.reason)
    txt = response.read().decode()
    print("REQUEST COMPLETED")

    file = open(f"{name}/split{i}.txt", "w")
    print("CREATED FILE", i)

    print("WRITING TO FILE")
    file.write(txt)
    file.close()
    conn.close()
    print(i, "COMPLETE")
print("TASK COMPLETE")
