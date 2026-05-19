DEBUG = True

class Equivalence:
    def __init__(self):
        self.white_equivalant = None
        self.black_equivalant = None
        self.resign_equivalent = None
        self.draw_equivalent = None
        self.check_stale_equivalent = None
        self.move_equivalent = None


def split_line(line :list):
    newline = list()
    i = 0
    while  i< len(line)-2 :
        if line[i] == '-' and line[i+1] == '-' and line[i+2] == '>':
            newline.append(line[:i].strip())
            tmp = (line[i+3:].split(':'))
            newline.append(tmp[0].strip())
            try:
                newline.append(tmp[1].strip())
            except:
                None
        i+=1

    return newline


def rewrite(f):
    dico = dict()

    copy =""

    line = f.readline()
    while line:
        copy += line
        if line[0] != "@":
            if "state" in line.lower() and "as" in line.lower():
                splitted = line.split()
                size = len(splitted)
                dico[splitted[size-1]] = " ".join(splitted[1:size-2]).replace("\"","")
        line = f.readline()
    result = ""

    lines = copy.splitlines()

    for l in lines:
        if l != "":
            if l[0] != "@":
                splitted = l.split()
                if len(splitted) >0 and splitted[0].lower() != "state":
                    for i in range(len(splitted)):
                        if splitted[i] in dico:
                            splitted[i] = dico[splitted[i]]
                    result+=" ".join(splitted)+"\n"

    return result


def replace(student_answer : list, Student : Equivalence, Result : Equivalence):

    for i in range(len(student_answer)):
        for j in range(len(student_answer[i])):
            match student_answer[i][j]:
                case Student.white_equivalant:
                    student_answer[i][j] = Result.white_equivalant
                case Student.black_equivalant:
                    student_answer[i][j] = Result.black_equivalant
                case Student.check_stale_equivalent:
                    student_answer[i][j] = Result.check_stale_equivalent
                case Student.resign_equivalent:
                    student_answer[i][j] = Result.resign_equivalent
                case Student.draw_equivalent:
                    student_answer[i][j] = Result.draw_equivalent
                case Student.move_equivalent:
                    student_answer[i][j] = Result.move_equivalent


def read_uml(file_name):

    file = open(file_name)

    if file == None :
        print("error opening file : {file_name}")
        exit(-2)

    rewrited_file = rewrite(file).splitlines()
    file.close()


    result = []

    #Add each line of the correction into a tab
    for l in rewrited_file:
        clean_line = l.replace("\n",'')
        # print(clean_line)
        result_line = split_line(clean_line)
        if result_line != []:
            result.append(result_line)

    return result


def preprocessor_wrapped(tab : list):

    eq = Equivalence()

    length_student = len(tab)

    # Check White
    # White is used as a "root" for finding other equivalance 
    i=0
    while i<length_student and eq.white_equivalant == None:
        if (tab[i][0] == '[*]'):
            eq.white_equivalant = tab[i][1]
        i+=1

    #If there is no white we stop here
    if eq.white_equivalant == None:
        return -1
    
    # check black
    for i in range(length_student):
        if tab[i][0] == eq.white_equivalant:
            for j in range(length_student):
                if tab[j][1] == eq.white_equivalant:
                    eq.black_equivalant = tab[j][0]

    # check stalemate/checkmate
    for i in range(length_student):
        if tab[i][0] == eq.white_equivalant and tab[i][1] == "[*]":
            try:
                if "check" in tab[i][2].lower() or "stale" in tab[i][2]:
                    eq.check_stale_equivalent = tab[i][2]
            except:
                pass

    
    # check resign
    i=0
    while i<length_student and eq.resign_equivalent == None:
        if tab[i][0] == eq.white_equivalant and tab[i][1] != eq.black_equivalant and tab[i][1] != eq.check_stale_equivalent \
            and ("res" in tab[i][1].lower() or "give up" in tab[i][1].lower() or "abandon" in tab[i][1].lower()):
            eq.resign_equivalent = tab[i][1]
        i+=1
    
    # check draw
    i=0
    while i<length_student and (eq.draw_equivalent == None or eq.draw_equivalent.lower() != "draw"):
        if tab[i][0] == eq.white_equivalant and tab[i][1] != eq.black_equivalant and tab[i][1] != eq.check_stale_equivalent and tab[i][1] != eq.resign_equivalent \
            and tab[i][1] != "[*]" and ("draw" in tab[i][1].lower() or "egal" in tab[i][1].lower() or "equal" in tab[i][1].lower()):
            eq.draw_equivalent = tab[i][1]
        i+=1


    #check move
    for i in range(length_student):
        if (tab[i][0] == eq.white_equivalant and tab[i][1] == eq.black_equivalant) or (tab[i][1] == eq.white_equivalant and tab[i][0] == eq.black_equivalant) :
            try:
                eq.move_equivalent = tab[i][2]
            except:
                pass

    return eq
                


def preprocessor(answer : list,student_answer : list):




    Student = preprocessor_wrapped(student_answer)
    if Student == -1:
        return -1
    Result = preprocessor_wrapped(answer)
    if Student == -1:
        return -2

    replace(student_answer,Student,Result)

    return 0
