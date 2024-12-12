import functions_framework
from google.cloud import bigquery
import json
from datetime import datetime, timedelta
import pandas as pd
from google.cloud import pubsub_v1


@functions_framework.http
def cfsizeCICD1(request):
    if request.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }
        print("responding to preflight ")
        return ("", 204, headers)

    request_json = request.get_json(silent=True)
    print("request_json:", request_json)
    ip_address = request.headers["x-forwarded-for"]
    current_timestamp = datetime.now()
    publisher = pubsub_v1.PublisherClient()
    request_logging_topic = (
        "projects/relevate-dev-403605/topics/relevate-ai-request-logging"
    )
    request_logging_data = json.dumps(
        {
            "cloudfunction": "relevate-ai-decile-report-data-insert1124567890011",
            "ipaddress": f"{ip_address}",
            "payload": request_json,
            "createdon": f"{current_timestamp}",
        }
    )
    data_bytes = request_logging_data.encode("utf-8")
    publisher.publish(request_logging_topic, data_bytes)
    bqclient = bigquery.Client()

    if "Id" in request_json:
        id_ = request_json.get("Id")
        print(id_)
        if id_ == "":
            print("Id is blank")
    else:
        print("Id is missing in payload")
        return "Id is missing in payload, please re-request with id Storage1237788990011286", 500
    
    if "Name" in request_json:
        Name_ = request_json.get("Name")
        print(Name_)
        if Name_ == "":
            print("Name is blank")
    else:
        print("Name is missing in payload")
        return "Name is missing in payload, please re-request with Name", 500

    try:
        insertquery = f"""
        INSERT INTO `RelevateSystem.InsertData_DevOps_POC` (Id,Name) 
        VALUES ({id_}, '{Name_}')
        """
        print("QuantityQuery:", insertquery)
        bqclient.query(insertquery).result()

    except Exception as e:
        return (
            json.dumps(
                {
                    "status": "Failed",
                    "message": f"Unable to load data for Id, Name: {id_}, {Name_}. Error: {str(e)}",
                }
            ),
            404,
            {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type, Authorization",
            },
        )

    return (
        json.dumps(
            {
                "status": "Success",
                "message": f"Successfully loaded data for Id, Name: {id_}, {Name_}",
            }
        ),
        200,
        {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        },
    )
