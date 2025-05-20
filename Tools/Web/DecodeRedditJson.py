import json
import requests
from pathlib import Path
import os
from markdown_it import MarkdownIt
import time

#TODO: Implement better rich text and actual media formatting

print("WARNING: This decoder does NOT support markdown or rich text or media embeds\n")

str_path = input("Enter file path, ex=[./file.json]\n:")
name = input("Directory name\n:")
custom_time = int(input("Enter yield time for requests [optional=10] [int]\n:") or 10)

SECURE = "https://"
SITE = "www.reddit.com"
MD = MarkdownIt("gfm-like")
MDS = MarkdownIt("commonmark", {"linkify":True})
TO_DIR = f"./r#{name}/"
HTML = """<!DOCTYPE html>
<html>
<meta charset="UTF-8">
<head>
<title>r/%SUB%</title>

<style>
.autoed {
    max-width: 100%;
    max-height: 80vh;
    height: auto;
}

ul, #myUL {
  list-style-type: none;
}

#myUL {
  margin: 0;
  padding: 0;
}

.caret {
  cursor: pointer;
  -webkit-user-select: none; /* Safari 3.1+ */
  -moz-user-select: none; /* Firefox 2+ */
  -ms-user-select: none; /* IE 10+ */
  user-select: none;
}

.caret::before {
  content: ">";
  color: black;
  display: inline-block;
  margin-right: 6px;
}

.caret-down::before {
  -ms-transform: rotate(90deg); /* IE 9 */
  -webkit-transform: rotate(90deg); /* Safari */'
  transform: rotate(90deg);  
}

.nested {
  display: none;
}

.active {
  display: block;
}

</style>
  
</head>
<body>

<small style="color:grey;font-family:Trebuchet MS;text-align:center;">by: u/%USER%<br>votes: %VOTES%</small>
<br>
<h2 style="font-family:Trebuchet MS;">%TITLE%</h2>

<p style="font-family:Trebuchet MS;">%SELF_BODY%</p>
<br>
<a href="%URL%" target="_blank">
%SRC%
</a>

<h2 style="font-family:Trebuchet MS;">%CMT_AMOUNT% Comments</h2>
<small>Click the &quot;&gt;&quot; icon to expand</small>
<br>

<ul id="myUL">
%COMMENTS%
</ul>

<script>
var toggler = document.getElementsByClassName("caret");
var i;

for (i = 0; i < toggler.length; i++) {
  toggler[i].addEventListener("click", function() {
    this.parentElement.querySelector(".nested").classList.toggle("active");
    this.classList.toggle("caret-down");
  });
}
</script>

</body>

</html>"""

def html_iframe(src):
    return f'<iframe class="autoed" src="{src}"></iframe>'

def html_image(src):
    return f'<img class="autoed" src="{src}" alt="link to post">'

def html_treeitem(message, auth, votes):
    return f'<li><small style="color:grey;">by: u/{auth} --- votes: {votes}</small><br>{message}</li><br>' + "\n"

def html_tree(message, auth, votes):
    return f'<li><span class="caret"><small style="color:grey;">by: u/{auth} --- votes: {votes}</small><br>{message}</span><ul class="nested">' + "\n", '</ul></li><br>' + "\n"

def get_comments(data):
    children = data["data"]["children"]
    s = ""
    for x in children:
        v = x["data"]
        message = MD.render(v["body"])
        votes = str(v["ups"] - v["downs"])
        auth = v["author"]
        if v.get("replies"):
            t_start, t_end = html_tree(message, auth, votes)
            s += t_start + get_comments(v["replies"]) + t_end
        else:
            s += html_treeitem(message, auth, votes)
    return s

file = open(str_path, "r", encoding="utf-8")

directory = Path(TO_DIR)
if not directory.exists():
    directory.mkdir()
    print("CREATED DIRECTORY")

decoded = json.load(file)

posts = decoded["data"]["children"]

consecutive = 1
encounters = dict()

for post in posts:
    v = post["data"]
    auth = v["author"]
    title = v["title"]
    body = v["selftext"]
    url = v["url"]

    file_dir = TO_DIR + auth
    if os.path.exists(file_dir):
        encounters[file_dir] = int(encounters.get(file_dir) or "0") + 1
        file_dir += f" [{encounters[file_dir]}]/"
    else:
        file_dir += "/"
    os.mkdir(file_dir)

    source = url
    if v.get("is_gallery"):
        gallery = v["gallery_data"]["items"]
        source = ""
        _link = v["permalink"].split("/")[-2]
        for x in gallery:
            source += html_image(f'https://preview.redd.it/{_link}-v0-{x["media_id"]}.png') + "<br>"
    else:
        source = html_image(url)
    
    contents = HTML.replace(
        "%SUB%", name
    ).replace(
        "%USER%", auth
    ).replace(
        "%SELF_BODY%", MD.render(body)
    ).replace(
        "%URL%", url
    ).replace(
        "%SRC%", source
    ).replace(
        "%TITLE%", title
    ).replace(
        "%VOTES%", str(v["ups"] - v["downs"])
    ).replace(
        "%CMT_AMOUNT%", str(v["num_comments"])
    )
    
    if v["num_comments"] > 0:
        if consecutive % 3 == 0:
            print("YIELDING...")
            time.sleep(custom_time)
        try:
            r = requests.get(SECURE + SITE + v["permalink"][:-1] + ".json")
            print("COMMENT STATUS:", r.status_code)
            print("GOT COMMENTS FOR", file_dir)
            r_decoded = json.loads(r.text)
            contents = contents.replace("%COMMENTS%", get_comments(r_decoded[1]))
            print("WROTE COMMENTS")
        except:
            print("ERR: FAILED TO FETCH OR WRITE COMMENTS")
            contents = contents.replace("%COMMENTS%", "FAILED TO FETCH COMMENTS")
        consecutive += 1
        time.sleep(1)
    else:
        contents = contents.replace("%COMMENTS%", "")

    with open(file_dir + "index.html", "w", encoding="utf-8") as new:
        new.write(contents)
    
    print("ENCODED:", file_dir)

with open(TO_DIR + "start.cmd", "w") as cmd_file:
    cmd_file.write("start chrome \"http://localhost:8000\"\npython -m http.server")

input("... TASK FINISHED ...")
