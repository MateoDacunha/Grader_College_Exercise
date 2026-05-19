from sys import argv
from textManage import *

correction_file = "test/V1_correction_chess/chess.correction"
note_max = 10

DEBUG=False




def evaluate(result : list, student_answer : list,note_max=10):

    final_grade = note_max


    for i in range(len(result)):
        verified_answer = False
        for j in range(len(student_answer)):
            if len(result[i]) == len(student_answer[j]) and not verified_answer:
                if result[i][0].lower() == student_answer[j][0].lower() and result[i][1].lower() == student_answer[j][1].lower():
                    if len(result[i]) == 3:
                        if result[i][2].lower() == student_answer[j][2].lower():
                            verified_answer = True
                    else:
                        verified_answer = True
            elif len(result[i]) >= len(student_answer[j]) and not verified_answer:
                if result[i][0].lower() == student_answer[j][0].lower() and result[i][1].lower() == student_answer[j][1].lower():
                    final_grade -= note_max/len(result)/2
                    verified_answer = True


        if not verified_answer:
            final_grade -= note_max/len(result)

    dif = len(student_answer) - len(result)
    if dif > 0:
        final_grade -= note_max/len(result)/2*dif

    if final_grade < 0.1:
        final_grade = 0

    return final_grade


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