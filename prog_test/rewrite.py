from sys import argv,path

path.append("..")

from textManage import rewrite


if len(argv) < 2:
        print("usage : python3 chess.py file_to_grade")
        exit(-1)

f = open(argv[1])

print(rewrite(f))

