#!/bin/bash

##
### TESTs
# curl http://localhost:5000/genericitemset
# curl http://localhost:5000/genericitem/Apple 
# curl http://localhost:5000/genericitem/Apple -d "IsCut=True"
# curl http://localhost:5000/genericitem/Brussels%20Sprouts -d "Subcategory=On%20Stem"
# curl http://localhost:5000/genericitemlist
# curl http://localhost:5000/matcheditemdict/Premium%20Bananas

ENDPOINT1="http://localhost:5000/genericitemset"
ENDPOINT2="http://localhost:5000/genericitem/Apple "
ENDPOINT3="http://localhost:5000/genericitem/Apple -d IsCut=True"
ENDPOINT4="http://localhost:5000/genericitem/Brussels%20Sprouts -d Subcategory=On%20Stem"
ENDPOINT5="http://localhost:5000/genericitemlist"
ENDPOINT6="http://localhost:5000/matcheditemdict/Premium%20Bananas"

trap "kill 0" EXIT 

python .../private_api/api.py &

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
