import json
import requests
from pathlib import Path
import os
from markdown_it import MarkdownIt
import time
import re
from datetime import datetime

print("WARNING: This decoder does not support extensive markdown or rich text or media embeds\n")

str_path = input("Enter file path, ex=[./file.json]\n:")
name = input("Directory name\n:")
get_comment_flag = input("Get comments? ['y'/'n'] [default='y']\n:").lower() or "y"
custom_time = 60
each_time = 2
if get_comment_flag == 'y':
    custom_time = int(input("Enter yield time for requests [default=60] [int]\n:") or custom_time)
    each_time = int(input("Each time [default=2] [int]\n:") or each_time)

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

.big = {
    height: 80%;
    width: 80%
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

<small style="color:grey;font-family:Trebuchet MS;text-align:center;">by: u/%USER%<br>votes: %VOTES%<br>at: %DATE%</small>
<br>
<h2 style="font-family:Trebuchet MS;">%TITLE%</h2>

<p style="font-family:Trebuchet MS;">%SELF_BODY%</p>
<br>
<a href="%URL%" target="_blank">
%SRC%
</a>

<h2 style="font-family:Trebuchet MS;">%CMT_AMOUNT% Comments</h2>
<small>Click the &quot;&gt;&quot; icon to expand<br></small>
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
    return f'<iframe class="big" src="{src}" title="link to embed" style="border:none;"></iframe>'

def html_video(src):
    return f'<video class="big" src="{src}" controls>no video</video>'

def html_image(src):
    return f'<img class="autoed" src="{src}" alt="link to media">'

def html_treeitem(message, auth, votes, date):
    return f'<li><small style="color:grey;">by: u/{auth} - votes: {votes} - at: {date}</small><br>{message}</li><br>' + "\n"

def html_tree(message, auth, votes, date):
    return f'<li><span class="caret"><small style="color:grey;">by: u/{auth} - votes: {votes} - at: {date}</small><br>{message}</span><ul class="nested">' + "\n", '</ul></li><br>' + "\n"

def get_time(created):
    return str(datetime.fromtimestamp(created))

def get_comments(data):
    children = data["data"]["children"]
    s = ""
    for x in children:
        v = x["data"]
        message = MD.render(v["body"])
        votes = str(v["ups"] - v["downs"])
        date = get_time(v["created"])
        auth = v["author"]
        if v.get("replies"):
            t_start, t_end = html_tree(message, auth, votes, date)
            s += t_start + get_comments(v["replies"]) + t_end
        else:
            s += html_treeitem(message, auth, votes, date)
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

errored = 0

for post in posts:
    v = post["data"]
    auth = v["author"]
    title = v["title"]
    body = v["selftext"]
    url = v["url"]
    date = v["created"]

    file_dir = TO_DIR + auth
    if os.path.exists(file_dir):
        encounters[file_dir] = int(encounters.get(file_dir) or "0") + 1
        file_dir += f" [{encounters[file_dir]}]/"
    else:
        file_dir += "/"
    os.mkdir(file_dir)

    source = url
    if v.get("is_gallery") and v.get("gallery_data"):
        gallery = v["gallery_data"]["items"]
        source = ""
        _link = v["permalink"].split("/")[-2]
        for x in gallery:
            source += html_iframe(f'https://preview.redd.it/{_link}-v0-{x["media_id"]}.png') + "<br>"
    elif v.get("is_video"):
        source = html_video(v["media"]["reddit_video"]["scrubber_media_url"])
    elif v.get("media_embed"):
        embed = re.search("src=\"(.+)\"", v["media_embed"]["content"])
        source = html_iframe(embed.group(1))
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
    ).replace(
        "%DATE%", get_time(date)
    )

    if v["num_comments"] > 0 and get_comment_flag == "y":
        time.sleep(each_time)
        if consecutive % 10 == 0:
            print("YIELDING...")
            time.sleep(custom_time)
        try:
            r = requests.get(SECURE + SITE + v["permalink"][:-1] + ".json")
            r.raise_for_status()
            print("GOT COMMENTS FOR", file_dir)
            r_decoded = json.loads(r.text)
            contents = contents.replace("%COMMENTS%", get_comments(r_decoded[1]))
            print("WROTE COMMENTS")
        except:
            print("ERR: FAILED TO FETCH OR WRITE COMMENTS")
            errored += 1
            contents = contents.replace("%COMMENTS%", "FAILED TO FETCH COMMENTS")
        consecutive += 1
    else:
        contents = contents.replace("%COMMENTS%", "COMMENTS WERE NOT ENABLED")

    with open(file_dir + "index.html", "w", encoding="utf-8") as new:
        new.write(contents)
    
    print("ENCODED:", file_dir)

with open(TO_DIR + "start.cmd", "w") as cmd_file:
    cmd_file.write("start chrome \"http://localhost:8000\"\npython -m http.server")

if get_comment_flag == "y":
    print(f"\nSuccessful comment fetches: {len(posts) - errored}\nFailed comment fetches: {errored}\n")

input("... TASK FINISHED ...")
