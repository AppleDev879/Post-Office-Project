import json

def lambda_handler(event, context):
    transactionID = event['queryStringParameters']['transactionId']
    transactionType = event['queryStringParameters']['type']
    print('transactionId=' + transactionID)
    
    #2 construct body of the response object
    transactionResponse = {}
    transactionResponse['transactionId'] = transactionID
    transactionResponse['type'] = transactionType
    
    #3. Construct http response object
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(transactionResponse)

    #4. Return the response object
    return responseObject

