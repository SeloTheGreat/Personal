import pathlib

DIRECTORY = input("Folder path to query split within, default='.\\split'\n:") or r".\split"

split_opt = input("Split='S' Merge='M'\n:").upper()
file = pathlib.Path(input("REQUIRED, Enter .txt file path to read/write (must be relative [name\\[...].txt])\n:"))

if split_opt == "S":
    folder = pathlib.Path(DIRECTORY)
    split_amount = int(input("Split amount=[int >= 2]\n:"))
    
    if split_amount < 2:
        raise ValueError("Split amount can't be smaller than 2")

    if not folder.exists():
        folder.mkdir()

    og_content = file.read_text()
    _len_ogcont = len(og_content)
    _def_split = _len_ogcont // split_amount
    _max_split = (_len_ogcont // split_amount) + _len_ogcont % split_amount
    
    contents = [
        og_content[_def_split*i:] if i == split_amount - 1 else og_content[_def_split*i:_def_split*(i+1)] for i in range(split_amount)
    ]

    counter = 0
    for s in contents:
        new_file = folder / f"split{counter}.txt"
        new_file.touch()
        new_file.write_text(s)

        print("SPLIT:", new_file)
        counter += 1
    
    print("TASK FINISHED")
elif split_opt == "M":
    folder = pathlib.Path(DIRECTORY)
    
    if not folder.exists():
        raise FileNotFoundError("Folder \"split\" doesn't exist")
    if not file.exists():
        file.touch()

    contents = ""
    
    counter = 0
    for query in folder.iterdir():
        new_file = folder / f"split{counter}.txt"
        contents += new_file.read_text()

        print("MERGED:", new_file)
        counter += 1
    print("WRITING TO SPECIFIED FILE")
    file.write_text(contents)
    print("TASK FINISHED")
else:
    print("Invalid input, input must be 'S' or 'M'")
