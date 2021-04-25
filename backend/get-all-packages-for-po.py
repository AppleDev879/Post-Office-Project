import json
import sys
import logging
import rds_config
import pymysql
import time

#rds settings
rds_host  = "post-office.clhbbeh0jkjv.us-east-2.rds.amazonaws.com"
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(host=rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")

def lambda_handler(event, context):
    conn.ping()
    with conn.cursor() as cur:
        qry = """SELECT p.TrackingNum, curLoc.Street_Address, recAddress.Street_Address
                FROM package p, package_status s, physical_address curLoc, physical_address recAddress, customer c
                WHERE s.Phys_ID = 3
                AND curLoc.Phys_ID = 3
                AND p.Receiver_ID = c.Customer_ID
                AND recAddress.Phys_ID = c.Phys_ID
                AND s.TrackingNum = p.TrackingNum;
                logger.info(qry)
                cur.execute(qry)
                """
        transactionResponse = cur.fetchall()
        
        cur.close()
        conn.close()

    #3. Construct http response object
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(transactionResponse)

    #4. Return the response object
    return responseObject

