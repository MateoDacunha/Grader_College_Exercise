from groq import Groq
import os
from sys import argv

DEBUG = True
def AI():

    note_max = 10
    correction_file = "test/V1_correction_chess/chess.correction"

    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),  # This is the default and can be omitted
    )

    result_file = open(correction_file)
    student_file= open(argv[1])

    result = result_file.read()
    student_answer = student_file.read()

    prompt = f"""
    You have 2 Text that represent UML state diagram of a chess game
    
    The first one is the result answer :
    {result}
    nbl define the number of line in result answer

    student_filename = {argv[1]} for this only keep the part V*_correction_chess/*.correction
    The second one is the student answer :
    {student_answer}

    First you need to change the answer of the student by following those steps :
    -In student_answer change the name of the state that match those from result if the meaning are the same,
    -A word A in the student_answer can only be changed by an only and unique (always the same) word B that is present in the correct result if the meaning are the same 
    -Remember that the first player is always white so '[*] --> XXX' means that XXX is always an equivalent to White you have to replace ALL XXX by White
    -There must be as many line at the output as there are at the input.

    Then you need to evaluate the student answer based on the result the note given is called final_grade which start a the value max_grade:
    - The maximum grade achievable is {note_max} called max_grade
    - For each line check if the same line is present in the student answer (we don't care about the difference of number of whitespace). If not take do final_grade -= max_grade/nbl
    - For each transition that should not be here do final_grade -= max_grade/nbl/2
    - At the end print an ONLY line like this : "The final grade for student_filename is final_grade/{note_max}"
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        # model="groq/compound",
        # model="openai/gpt-oss-20b",
        model="openai/gpt-oss-120b",
        # model="meta-llama/llama-4-scout-17b-16e-instruct",
        max_tokens=6500

    )

    if DEBUG:
        print(chat_completion.usage)
        print();print()

    print(chat_completion.choices[0].message.content)



    return

if __name__ == "__main__":
    AI()