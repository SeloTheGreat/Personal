from uuid import uuid4
from pathlib import Path

print("!IMPORTANT! This script only supports .lua/.luau files and only uses module scripts, it's extrimely primitive and only intended for specific purposes\n")

dir_path = input("Enter path to encode to .rbxmx, ex='.\\my_directory'\n:")

source_start = "<roblox xmlns:xmime=\"http://www.w3.org/2005/05/xmlmime\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:noNamespaceSchemaLocation=\"http://www.roblox.com/roblox.xsd\" version=\"4\">\n<Meta name=\"ExplicitAutoJoints\">true</Meta>\n<External>null</External>\n<External>nil</External>"
source = ""
source_end = "</roblox>"

def xmlitem(item_class):
    return f"<Item class=\"{item_class}\" referent=\"RBX{str(uuid4())}\">", "</Item>"

def xmlproperties():
    return "<Properties>", "</Properties>"

def xmlproperty(property_type, name, value):
    return f"<{property_type} name=\"{name}\">", f"{value}", f"</{property_type}>"

def cdata(s):
    return f"<![CDATA[{s}]]>"

def encode_folder(query, children=""):
    item1, item2 = xmlitem("Folder")
    prop1, prop2 = xmlproperties()
    name1, nameval, name2 = xmlproperty("string", "Name", query.stem)

    return_item = item1 + prop1 + name1 + nameval + name2 + prop2
    if children:
        for v in children:
            return_item += v
    
    return return_item + item2

def encode_module(query, children="", name=""):
    item1, item2 = xmlitem("ModuleScript")
    prop1, prop2 = xmlproperties()
    name1, nameval, name2 = xmlproperty("string", "Name", name or query.stem)
    source1, sourceval, source2 = xmlproperty("ProtectedString", "Source", cdata(query.read_text()))

    return_item = item1 + prop1 + name1 + nameval + name2 + source1 + sourceval + source2 + prop2
    if children:
        for v in children:
            return_item += v
    
    return return_item + item2

def encode_script(query, runContext=0, children="", name=""):
    script_class = "Script"
    if runContext == 1:
        script_class = "Script"
    elif runContext == 2:
        script_class = "LocalScript"
    item1, item2 = xmlitem(script_class)
    prop1, prop2 = xmlproperties()
    name1, nameval, name2 = xmlproperty("string", "Name", name or query.stem.split(".")[0])
    source1, sourceval, source2 = xmlproperty("ProtectedString", "Source", cdata(query.read_text()))

    return_item = item1 + prop1 + name1 + nameval + name2 + source1 + sourceval + source2 + prop2
    if children:
        for v in children:
            return_item += v
    
    return return_item + item2

def encode(iterf, parent):
    print("IN DIRECTORY:", parent)
    
    folder_items = []

    init_query = None
    
    for query in iterf():
        if query.is_dir():
            folder_items.append(encode(query.iterdir, query))
        elif query.suffix == ".lua" or query.suffix == ".luau":
            if query.stem.split(".")[0] == "init":
                init_query = query
            elif query.suffixes[0] == ".client":
                folder_items.append(encode_script(query, 2))
            elif query.suffixes[0] == ".server":
                folder_items.append(encode_script(query, 1))
            elif query.suffixes[0] == ".legacy":
                folder_items.append(encode_script(query, 0))
            else:
                folder_items.append(encode_module(query))
            print("ENCODED:", query)
    if init_query:
        if init_query.suffixes[0] == ".client":
            folder_str = encode_script(init_query, 2, folder_items, parent.stem)
        elif init_query.suffixes[0] == ".server":
            folder_str = encode_script(init_query, 1, folder_items, parent.stem)
        elif init_query.suffixes[0] == ".legacy":
            folder_str = encode_script(init_query, 0, folder_items, parent.stem)
        else:
            folder_str = encode_module(init_query, folder_items, parent.stem)
    else:
        folder_str = encode_folder(parent, folder_items)

    print("FINISHED", parent)

    return folder_str

directory = Path(dir_path)

source += encode(directory.iterdir, directory)

file = open(dir_path + ".rbxmx", mode="w")
file.write(
    source_start + "\n" + source + "\n" + source_end
)
file.close()
input("... FINISHED ...")
