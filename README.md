> *School Location = Turkey/Türkiye*

# School

Hello! This is my personel stuff related to school...
Don't use the things here, if you are reading this please don't, they are not supposed to be used for anything. The only reason it is  documented at all is so that I don't forget things.

---

## Data

This folder is for holding data... Simple as that

---

## Tools

This folder is for holding tools... Simple as that

### Converter.py

This script is used to encode and decode file trees into single txt files. This is due to downloading being blocked on my school computers,
so I have to resort to this instead.

**Inputs:**
1. Input will ask for you to enter "E" or "D" respectively stands for encode and decode, note that the input is not case-senstive
2. Input will ask for a plain string that only allows file-name-appropriate character, this decides the folder/file the script will use for querying with the 3. input
3. Input will ask for a Path, this string is later used with input 2 to use `pathlib.Path` to create a path to the desired file/folder

*Only been used for atleast [python 3.9](https://www.python.org/downloads/release/python-390/) or higher*

### ConverterSplit.py

This script is used to split .txt files into multiple ones so my poor self can use lsf for slightly larger files

**Inputs:**
1. TODO

*Only been used for atleast [python 3.9](https://www.python.org/downloads/release/python-390/) or higher*

### GetRequest.py

This script performs a get request from specified url and writes it to a specified file

*Only been used for atleast [python 3.9](https://www.python.org/downloads/release/python-390/)*

---

## WindowsCMD

***Only works with Windows Command Prompt, only been tested on Windows 10***

Use `setup.bat` to set up the .cmd files to allow for quick access or optionally, manually use the .cmd files on their own

Here is a list of all cmds:
- vpip

"help" as first argument provides info on each command