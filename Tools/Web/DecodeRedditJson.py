import json
import requests
from pathlib import Path
import os

str_path = input("Enter file path, ex=[./file.json]\n:")
name = input("Directory name\n:")

TO_DIR = f"./r#{name}/"
HTML = """<!DOCTYPE html>
<html>
<head>
<title>r/%SUB%</title>

<style>
img.autoed {
    max-width: 100%;
    max-height: 80vh;
    height: auto;
}
</style>
  
</head>
<body>

<small style="color:grey;font-family:Trebuchet MS;text-align:center;">post by u/%USER%</small>
<br>
<p style="font-family:Trebuchet MS;">%SELF_TXT%</p>
<br>
<img class="autoed" src="%URL%" alt="this is ass lol">

</body>
</html>"""

file = open(str_path, "r", encoding="utf-8")

directory = Path(TO_DIR)
if not directory.exists():
    directory.mkdir()
    print("CREATED DIRECTORY")

decoded = json.load(file)

posts = decoded["data"]["children"]

for post in posts:
    v = post["data"]
    auth = v["author"]
    title = v["title"]
    body = v["selftext"]
    url = v["url"]

    file_dir = TO_DIR + f"u#{auth}"
    if os.path.exists(file_dir):
        file_dir += " [1]/"
    else:
        file_dir += "/"
    os.mkdir(file_dir)
    
    contents = HTML.replace("%SUB%", name).replace("%USER%", auth).replace("%SELF_TXT%", body).replace("%URL%", url)

    with open(file_dir + "index.html", "w") as new:
        new.write(contents)
    
    print("ENCODED:", file_dir)

input("... TASK FINISHED ...")
