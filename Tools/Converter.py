import pathlib
import re
import zlib
import base64

option = input("Encode='E' Decode='D'\n:").upper()

ENTRY_KEY = "$"

_NAME = input("REQUIRED, Enter name to query folder/.txt file with, is=[str]\n:")
_PATH = input("Folder path to query file within, default=\"\"\n:") or "."
FOLDER_PATH = _PATH + "\\" + _NAME
FILE_NAME = f"{_PATH}\\{_NAME}.txt"
BS = "\\"

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
    print("TASK FINISHED")
elif option == 'D':
    f = open(FILE_NAME, 'r')
    s = f.read().split(ENTRY_KEY)
    s.pop()
    directory = pathlib.Path(FOLDER_PATH)
    if not directory.exists():
        directory.mkdir()
    decode(s, directory)
    f.close()
    print("TASK FINISHED")
else:
    print("Invalid input, input must be 'E' or 'D'")
