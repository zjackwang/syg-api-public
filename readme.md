## SaveYourGroceries API Server

### Required HTTP Request Headers 
1. X-Syg-Api-Key: Public key assigned to client 
2. X-Hmac-Signature: HMAC signature generated from request payload and client's private key 

### Running API tests from root dir 

1. HTTP Requests
   python run_tests.py http --loc local
      - testing localhost endpoints
   python run_tests.py http --loc remote
      - testing deployed endpoints

2. MongoDB Requests
   python run_tests.py mongo 