from http import client

print("NOTE: this script only provides basic request needs, headers and arguments, retries are not supported")

name = input("Enter name of file including any extensions, leave blank for def=\"new_req.txt\"\n:") or "new_req.txt"
url = input("Enter pure host site url to perform a get request from ex=[raw.githubuser.com]\n:")
access = input("Enter pure access url [n1/n2/...], def='/'\n:")
conn_type = input("ConType: 'HTTPS'|'HTTP'").upper()

print("REQUESTING")
conn = client.HTTPSConnection(url) if conn_type == "HTTPS" else client.HTTPConnection(url)
conn.request("GET", access)
response = conn.getresponse()
print("RESPONSE STATUS:", response.status, response.reason)
txt = response.read().decode()
print("REQUEST COMPLETED")

file = open(name, "w")
print("CREATED FILE", name)

print("WRITING TO FILE")
file.write(txt)
file.close()
conn.close()
print("TASK COMPLETE")
