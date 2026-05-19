PROG=("chess_V1.py" "chess_V2.py" "chess_V3.py" "chess_V4.py")
FOLDER=("test/V1_correction_chess/*.correction" "test/V2_correction_chess/*.correction" "test/exoUML/*")

#"V2_correction_chess/*.correction" "exoUML/*"

PYTHON_VERSION=.venv/bin/python3

BLUE='\033[0;94m'
GREEN='\033[0;92m'
RED='\033[0;91m'
NC='\033[0;0;0m'

echo "File,V1,V2,V3,V4" > grade.csv

writeResult () {
    exit_output=$?
    res=$(echo $2  | tr -s ' ' '\n' | tail -n 1)
    res=$(echo $res | tr '/' '\n' | head -n 1)
    if [[ ${res%.*} -ge 0 && $exit_output -eq 0 ]]
    then 
        if [ $3 = "chess_V4.py" ]
        then
            echo "$res" >> grade.csv
        else 
            echo -n "$res," >> grade.csv
        fi
    else 
        if [ $3 = "chess_V4.py" ]
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
        sleep 60
    done
done