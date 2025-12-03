import pathlib
import re
import zlib
import base64

ENTRY_KEY = "$"
BS = "\\"
NL = "\n"

ALIASES = dict()
alias_file = pathlib.Path(".aliases")
if alias_file.exists():
    alias_content = alias_file.read_text(encoding="utf-8").split("$")
    alias_content.pop(0)
    alias_content.pop()
    for v in alias_content:
        alias_properties = v.split("\n")
        alias_properties.pop(0)
        alias_properties.pop()
        new_alias = dict()
        for s in alias_properties:
            prop = s.split("|")
            assert len(prop) == 2
            new_alias[prop[0]] = prop[1]
        ALIASES[new_alias["name"]] = new_alias

if True:
    alias_log = "ALIASES:\n"
    if len(ALIASES) > 1:
        for s in ALIASES.values():
            alias_log += "• "+ s["name"] + " {\n\tinput = \"" + s["input"] + "\"\n\toutput = \"" + s["output"] + "\"\n}\n"
    else:
        alias_log += "• No aliases found in current working directory"
    print(alias_log + "\n")

print("PLEASE ENTER OPTIONS BELOW:\n")

option = input("Mode: Encode='E' Decode='D'\n:").upper()
_NAME = input("Enter name to query folder/.txt file with, or an ALIAS, is=[str]\n:")
_PATH = ""

FOLDER_PATH = ""
FILE_NAME = ""

GOT_ALIAS = ALIASES.get(_NAME)
if GOT_ALIAS:
    print("\nGot alias \"" + GOT_ALIAS["name"] + "\"")
    FOLDER_PATH = GOT_ALIAS["input"]
    FILE_NAME = GOT_ALIAS["output"]
else:
    _PATH = input("Folder path to query file within, default=\"\"\n:") or "."
    FOLDER_PATH = _PATH + "\\" + _NAME
    FILE_NAME = f"{_PATH}\\{_NAME}.txt"

file_contents = ''

def get_content_bytes(data, encode_set):
    return base64.b64encode(zlib.compress(data)).decode() if encode_set else zlib.decompress(base64.b64decode(data.encode()))

def encode(iterf, parent):
    print("IN DIRECTORY:", parent)
    has_children = False
    for query in iterf():
        has_children = True
        if query.is_dir():
            encode(query.iterdir, f"{parent}{BS}{query.name}")
        else:
            global file_contents
            str_contents = get_content_bytes(query.read_bytes(), True)
            file_contents += f"{parent + BS + query.name}:{str_contents}{ENTRY_KEY}"
            print("ENCODED:", query)
    if not has_children:
        file_contents += f"{parent}:~{ENTRY_KEY}"

def decode(split, top_directory):
    for sfile in split:
        matched = re.match("^(.+):", sfile)
        
        nfile = matched.group(1).replace(".", FOLDER_PATH, 1)
        file = pathlib.Path(nfile)
        
        real_contents = sfile[matched.end():]
        
        if real_contents == '~':
            file.mkdir(parents=True)
            continue
        
        contents = get_content_bytes(real_contents, False)
        
        if not file.parent.exists():
            file.parent.mkdir(parents=True)
        file.touch()
        
        file.write_bytes(contents)
        print("DECODED:", nfile)

if option == 'E':
    directory = pathlib.Path(FOLDER_PATH)
    f = open(FILE_NAME, 'w')
    encode(directory.iterdir, '.')
    print("WRITING TO FILE")
    f.write(file_contents)
    f.close()
    input("... TASK FINISHED ...")
elif option == 'D':
    f = open(FILE_NAME, 'r')
    s = f.read().split(ENTRY_KEY)
    s.pop()
    directory = pathlib.Path(FOLDER_PATH)
    if not directory.exists():
        directory.mkdir()
    decode(s, directory)
    f.close()
    input("... TASK FINISHED ...")
else:
    input("... Invalid mode input, mode input must be 'E' (encode) or 'D' (decode) ...")
