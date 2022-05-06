#!/bin/bash

##
### TESTs
ENDPOINT1="https://api-syg.herokuapp.com/genericitemset"
ENDPOINT2="https://api-syg.herokuapp.com/genericitem/Apple"
ENDPOINT3="https://api-syg.herokuapp.com/genericitem/Apple -d IsCut=True"
ENDPOINT4="https://api-syg.herokuapp.com/genericitem/Brussels%20Sprouts -d Subcategory=On%20Stem"
ENDPOINT5="https://api-syg.herokuapp.com/genericitemlist"
ENDPOINT6="https://api-syg.herokuapp.com/matcheditemdict/Premium%20Bananas"

trap "kill 0" EXIT 

python ../private_api/api.py &

sleep 2
echo "***Testing endpoint $ENDPOINT1***"
returned_code="$(curl -L $ENDPOINT1 -o /dev/null -w '%{http_code}\n' -s)"
if [[ $returned_code != 200 ]]; then 
    echo "=> Failed with code $returned_code"
else 
    echo "Success!"
fi

echo "***Testing endpoint $ENDPOINT2***"
returned_code="$(curl -L $ENDPOINT2 -o /dev/null -w '%{http_code}\n' -s)"
if [[ $returned_code != 200 ]]; then 
    echo "=> Failed with code $returned_code"
else 
    echo "Success!"
fi

echo "***Testing endpoint $ENDPOINT3***"
returned_code="$(curl -L $ENDPOINT3 -o /dev/null -w '%{http_code}\n' -s)"
if [[ $returned_code != 200 ]]; then 
    echo "=> Failed with code $returned_code"
else 
    echo "Success!"
fi

echo "***Testing endpoint $ENDPOINT4***"
returned_code="$(curl -L $ENDPOINT4 -o /dev/null -w '%{http_code}\n' -s)"
if [[ $returned_code != 200 ]]; then 
    echo "=> Failed with code $returned_code"
else 
    echo "Success!"
fi


echo "***Testing endpoint $ENDPOINT5***"
returned_code="$(curl -L $ENDPOINT5 -o /dev/null -w '%{http_code}\n' -s)"
if [[ $returned_code != 200 ]]; then 
    echo "=> Failed with code $returned_code"
else 
    echo "Success!"
fi


echo "***Testing endpoint $ENDPOINT6***"
returned_code="$(curl -L $ENDPOINT6 -o /dev/null -w '%{http_code}\n' -s)"
if [[ $returned_code != 200 ]]; then 
    echo "=> Failed with code $returned_code"
else 
    echo "Success!"
fi
