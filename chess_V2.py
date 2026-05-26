from sys import argv
from textManage import *
from chess_V1 import evaluate

correction_file = "test/V1_correction_chess/chess.correction"
note_max = 10

DEBUG=True

def main():

    if len(argv) < 2:
        print("usage : python3 chess.py file_to_grade")
        exit(-1)

    #Get the correction
    result = read_uml(correction_file)

    #Student part
    student_answer = read_uml(argv[1])

    # Launch of the preprocessor
    err = preprocessor(result,student_answer)

    if DEBUG:
        for i in range(len(student_answer)):
            print(student_answer[i])
    
    if err == -1:
        print("No initial state was found in {0}".format(argv[1]))
        exit(-3)
    elif err == -2:
        print("No initial state was found in {0}".format(correction_file))
        exit(-3)
    
    final_grade = evaluate(result,student_answer)
    print("The final grade for {0} is {1}/{2}".format(argv[1],round(final_grade,1),note_max))
    return final_grade

if __name__ == "__main__":
    main()