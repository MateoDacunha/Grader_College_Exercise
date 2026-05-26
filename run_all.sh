if [ $# -ne 0 ] && [ $1 = "-h" ]
then
    echo "usage run_all.sh <val1> <val2>"
    echo "if no parameters are entered it run every program with every test"
    echo "  val1 :"
    echo "      -h print this help"
    echo "      int [0;15] a sum of value for program with chess_V1.py = 1, chess_V2.py = 2, chess_V3.py = 4, chess_V4.py = 8"
    echo "  val2 :"
    echo "      int [0;31] a sum of value for test with V1_correction_chess = 1, V2_correction_chess = 2, exoUML = 4, CP = 8, MT=16"

    exit
fi

echo -n "File" > grade.csv

if [ $# -eq 0 ]
then 
    PROG=("chess_V1.py" "chess_V2.py" "chess_V3.py" "chess_V4.py")
else
    val=$1
    FOLDER=()
    if [ $(($val&1)) -ne 0 ]
    then
        PROG+=("chess_V1.py")
        echo ",V1" >> grade.csv
    fi
    if [ $(($val&2)) -ne 0 ]
    then
        PROG+=("chess_V2.py")
        echo ",V2" >> grade.csv
    fi
    if [ $(($val&4)) -ne 0 ]
    then
        PROG+=("chess_V3.py")
        echo ",V3" >> grade.csv
    fi
    if [ $(($val&8)) -ne 0 ]
    then
        PROG+=("chess_V4.py")
        echo ",V4" >> grade.csv
    fi
fi


if [ $# -lt 2 ]
then 
    FOLDER=("test/V1_correction_chess/*.correction" "test/V2_correction_chess/*.correction" "test/exoUML/*" "test/CP/*" "test/MT/*")
else
    val=$2
    FOLDER=()
    if [ $(($val&1)) -ne 0 ]
    then
        FOLDER+=("test/V1_correction_chess/*.correction")
    fi
    if [ $(($val&2)) -ne 0 ]
    then
        FOLDER+=("test/V2_correction_chess/*.correction")
    fi
    if [ $(($val&4)) -ne 0 ]
    then
        FOLDER+=("test/exoUML/*")
    fi
    if [ $(($val&8)) -ne 0 ]
    then
        FOLDER+=("test/CP/*")
    fi
    if [ $(($val&16)) -ne 0 ]
    then
        FOLDER+=("test/MT/*")
    fi
fi



PYTHON_VERSION=.venv/bin/python3

BLUE='\033[0;94m'
GREEN='\033[0;92m'
RED='\033[0;91m'
NC='\033[0;0;0m'



writeResult () {
    exit_output=$?
    res=$(echo $2  | tr -s ' ' '\n' | tail -n 1)
    res=$(echo $res | tr '/' '\n' | head -n 1)
    if [[ ${res%.*} -ge 0 && $exit_output -eq 0 ]]
    then 
        if [ $3 = ${PROG[@]: -1} ]
        then
            echo "$res" >> grade.csv
        else 
            echo -n "$res," >> grade.csv
        fi
    else 
        if [ $3 = ${PROG[@]: -1} ]
        then
            echo "0" >> grade.csv
        else 
            echo -n "0," >> grade.csv
        fi
    fi
}

for f in ${FOLDER[@]}
do
    for file in $f
    do
    echo -n $file, >> "grade.csv"
        for p in ${PROG[@]}
        do
            echo -e running file :${GREEN}$file${NC} with program : ${BLUE}$p${NC}
            result=$($PYTHON_VERSION $p $file)
            writeResult $file "$result" $p
        done 
        if [ $# -ne 0 ] && [ $(($1&8)) -ne 0 ] # too much token so have to wait if we do AI
        then
            sleep 65
        fi
    done
done