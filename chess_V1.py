from sys import argv

correction_file = "test/V1_correction_chess/chess.correction"
note_max = 10
DEBUG = False


def split_line(line):
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


def evaluate(result,student_answer):

    final_grade = note_max

    if len(student_answer) < 1:
        return 0

    for i in range(len(result)): # For each line in the correction
        verified_answer = False
        for j in range(len(student_answer)): # we compare for each line in the student's answer
            if len(result[i]) == len(student_answer[j]) and not verified_answer:
                #if there is a match then the answer is confirmed and the student don't lose point for this part of the correction
                if result[i][0].lower() == student_answer[j][0].lower() and result[i][1].lower() == student_answer[j][1].lower(): 
                    if len(result[i]) == 3:
                        if result[i][2].lower() == student_answer[j][2].lower():
                            verified_answer = True
                    else:
                        verified_answer = True
            #in the case where the student misses the condition on the transition they loose half what they are supposed to loose
            elif len(result[i]) >= len(student_answer[j]) and not verified_answer:
                if result[i][0].lower() == student_answer[j][0].lower() and result[i][1].lower() == student_answer[j][1].lower():
                    final_grade -= note_max/len(result)/2
                    verified_answer = True
                    if DEBUG:
                        print("({})".format(i))



        if not verified_answer:
            final_grade -= note_max/len(result)


    dif = len(student_answer) - len(result)
    if dif > 0:
        final_grade -= note_max/len(result)/2*dif
        print("Here")

    
    if final_grade < 0.1:
        final_grade = 0

    return final_grade


def read_uml(file_name):

    file = open(file_name)
    if file == None :
        print("error opening file : {file_name}")
        exit(-2)


    line = file.readline()  
    result = []

    #Add each line of the correction into a tab
    while line:
        clean_line = line.replace("\n",'')
        # print(clean_line)
        result_line = split_line(clean_line)
        if result_line != []:
            result.append(result_line)
        line = file.readline()

    file.close()
    return result


def main():

    if len(argv) < 2:
        print("usage : python3 chess.py file_to_grade")
        exit(-1)

    #Get the correction
    result = read_uml(correction_file)

    #Student part
    student_answer = read_uml(argv[1])
    
    final_grade = evaluate(result,student_answer)
    print("The final grade for {0} is {1}/{2}".format(argv[1],round(final_grade,1),note_max))
    return final_grade

if __name__== "__main__":   
    main()