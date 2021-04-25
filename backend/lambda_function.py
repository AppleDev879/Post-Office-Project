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
    """
    This function fetches content from MySQL RDS instance
    """
    t = time.strftime('%Y-%m-%d %H:%M:%S')
    passedStatus = event.get('status','none')
    phys_id = event.get('phys_id', 0)
    tracking_num = event.get('tracking_num', 0)
    
    # Check to make sure the tracking num exists
    with conn.cursor() as cur:
        qry = """SELECT COUNT(*)
                FROM package
                WHERE TrackingNum = %s;"""%(tracking_num)
        cur.execute(qry)
        body = cur.fetchone()
        
    if (body[0] == 0):
        return {
            'statusCode': 404,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Credentials': 'true',
                'Content-Type': 'application/json'
            },
            'body': {"error": "Could not locate packages with the Tracking Number %d."%(tracking_num)}
        }
    
    with conn.cursor() as cur:
        qry = """INSERT INTO package_status (`Status`, Phys_ID, TimeEntered, TrackingNum)
            VALUES (\"%s\", %d, \"%s\", %d);"""%(passedStatus, phys_id, t, tracking_num)
        logger.info(qry)
        cur.execute(qry)
        body = cur.fetchall()
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Credentials': 'true',
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body)
    }
