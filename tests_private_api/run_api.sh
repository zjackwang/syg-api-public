#!/bin/bash

source .config

hmac_sig="$(python ../../security/hmac_sig_gen.py --key $PRIVATE_API_SECRET_KEY)"
TEST_ENDPOINT="-H X-Syg-Api-Key:$PRIVATE_API_PUBLIC_KEY -H X-HMAC-Signature:$hmac_sig http://localhost:5000/genericitem/Apple -d IsCut=True"

trap "kill 0" EXIT 

python ../api.py &

sleep 2
echo "***Testing endpoint $TEST_ENDPOINT***"
returned_code="$(curl $TEST_ENDPOINT)"