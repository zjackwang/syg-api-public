## SaveYourGroceries API Server

### Required HTTP Request Headers 
1. X-Syg-Api-Key: Public key assigned to client 
2. X-Hmac-Signature: HMAC signature generated from request payload and client's private key 
3. X-Hmac-Message: String message used to generated hmac signature

### Endpoints 
#### /genericitem/<generic_item_name>
~~GET~~
~~- queries specific generic item that match "generic_item_name" ~~
POST 
- parameterized query for generic items that match given "generic_item_name" and JSON params
- JSON params: 
   - isCut : Bool
   - isCooked : Bool
   - isOpened : Bool
   - subcategory : String 
#### /genericitemset
GET 
- returns all generic items 
#### /genericitemlist
GET 
- returns all generic item names 
#### /matcheditemdict
POST
- returns matched generic item  or returns 404 doesn't exist if so
- JSON params:
   - scanned_item_name: String 

### Running API tests from root dir 

1. HTTP Requests
   python run_tests.py http --loc local
      - testing localhost endpoints
   python run_tests.py http --loc remote
      - testing deployed endpoints

2. MongoDB Requests
   python run_tests.py mongo 

