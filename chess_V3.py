from groq import Groq
import os
from sys import argv
from chess_V1 import read_uml,evaluate


def string_to_list(String):
    result = []
    current_list = []
    current_word = ""
    inside_string = False

    for char in String:
        if char == "'":
            inside_string = not inside_string
            if not inside_string:
                current_list.append(current_word)
                current_word = ""

        elif inside_string:
            current_word += char

        elif char == "[":
            # Only create a new sublist if we're not already inside one
            if current_list is None:
                current_list = []

        elif char == "]":
            if current_list is not None:
                result.append(current_list)
                current_list = None

    return result

def main():

    note_max = 10
    correction_file = "test/V1_correction_chess/chess.correction"
    student_file = argv[1]

    result = read_uml(correction_file)
    student_answer = read_uml(student_file)

    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),  # This is the default and can be omitted
    )

    prompt = f"""
    Here is the student answer : {student_answer}
    And here is the correct result {result}

    -In student_answer change the name of the state that match those from result if the meaning are the same,
    -A word A in the student_answer can only be changed by an only and unique (always the same) word B that is present in the correct result if the meaning are the same 
    -Remember that the first player is always white so '[*] --> XXX' means that XXX is always an equivalent to White you have to replace ALL XXX by White
    -There must be as many index at the output as there are at the input. 
    -Then print only student_answer modified
    """


    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="openai/gpt-oss-120b",
        max_tokens=5000

    )

    print(chat_completion.choices[0].message.content)

    print("###############")
    print(chat_completion.usage)
    print("###############")



    student_answer = string_to_list(chat_completion.choices[0].message.content)
    for i in range(len(student_answer)):
        print(student_answer[i])
    final_grade = evaluate(result,student_answer)
    print("The final grade for {0} is {1}/{2}".format(argv[1],round(final_grade,1),note_max))

if __name__=="__main__":
    main()