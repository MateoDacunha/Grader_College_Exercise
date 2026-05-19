PYTHON_FILE=chess_V3.py

# PYTHON_VERSION=python3
PYTHON_VERSION=.venv/bin/python3

BLUE='\033[0;94m'
GREEN='\033[0;92m'
RED='\033[0;91m'
NC='\033[0;0;0m'

MAX_GRADE=10

isTestValid () {
    exit_output=$?
    res=$(echo $2  | tr -s ' ' '\n' | tail -n 1)
    res=$(echo $res | tr '/' '\n' | head -n 1)
    if [[ ${res%.*} -ge 0 && $exit_output -eq 0 ]]
    then 
        echo -e ${GREEN}Test Passed${NC} file : $1 with a grade of ${BLUE}$res/$MAX_GRADE${NC}
    else 
        echo -e ${RED}Test Failed${NC} file : $1
    fi
    echo
}

for file in V1_correction_chess/*.correction;
do
    result=$($PYTHON_VERSION $PYTHON_FILE $file)
    isTestValid $file "$result"
done

for file in V2_correction_chess/*.correction;
do
    result=$($PYTHON_VERSION $PYTHON_FILE $file)
    isTestValid $file "$result"
done

for file in exoUML/*;
do
    result=$($PYTHON_VERSION $PYTHON_FILE $file)
    isTestValid $file "$result"
done