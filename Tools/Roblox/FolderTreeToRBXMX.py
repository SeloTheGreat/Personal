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

def encode_folder(query, children):
    item1, item2 = xmlitem("Folder")
    prop1, prop2 = xmlproperties()
    name1, nameval, name2 = xmlproperty("string", "Name", query.stem)

    return_item = item1 + prop1 + name1 + nameval + name2 + prop2
    for v in children:
        return_item += v
    
    return return_item + item2

def encode_module(query):
    item1, item2 = xmlitem("ModuleScript")
    prop1, prop2 = xmlproperties()
    name1, nameval, name2 = xmlproperty("string", "Name", query.stem)
    source1, sourceval, source2 = xmlproperty("ProtectedString", "Source", cdata(query.read_text()))
    return item1 + prop1 + name1 + nameval + name2 + source1 + sourceval + source2 + prop2 + item2

def encode_script(query, runContext=0):
    item1, item2 = xmlitem("Script")
    prop1, prop2 = xmlproperties()
    name1, nameval, name2 = xmlproperty("string", "Name", query.stem.split(".")[0])
    context1, contextval, context2 = xmlproperty("token", "RunContext", runContext)
    source1, sourceval, source2 = xmlproperty("ProtectedString", "Source", cdata(query.read_text()))
    return item1 + prop1 + name1 + nameval + name2 + context1 + contextval + context2 + source1 + sourceval + source2 + prop2 + item2

def encode(iterf, parent):
    print("IN DIRECTORY:", parent)
    
    folder_items = []
    
    for query in iterf():
        if query.is_dir():
            folder_items.append(encode(query.iterdir, query))
        elif query.suffix == ".lua" or query.suffix == ".luau":
            if query.suffixes[0] == ".client":
                folder_items.append(encode_script(query, 2))
            elif query.suffixes[0] == ".server":
                folder_items.append(encode_script(query, 1))
            elif query.suffixes[0] == ".legacy":
                folder_items.append(encode_script(query, 0))
            else:
                folder_items.append(encode_module(query))
            print("ENCODED:", query)
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
