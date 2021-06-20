import os
import yaml
from flask import Flask
from flask import request, jsonify

from delete import delete
from ls import ls
from sas import upload_blob_sas, download_blob_sas
from upload import upload
from datetime import datetime, timedelta
from validation import SasRequestSchema, ListRequestSchema, DeleteRequestSchema

app = Flask(__name__)


def load_config():
    dir_root = os.path.dirname(os.path.abspath(__file__))
    with open(dir_root + "/config.yaml", "r") as yamlfile:
        return yaml.load(yamlfile, Loader=yaml.FullLoader)


'''
Generates a SAS for uploading to a Container in Azure

 Endpoint: /upload
 Method: Get
 Content-type: Application/json
 Request-body: { 
                    "container_name" : <CONTAINER_NAME>,
                    "blob_name" : <BLOB_NAME>
               }
 Response: 
            1. OK - 200
                    Response-body : {
                                        "uri": <URI>,
                                        "container_name": <CONTAINER_NAME>,
                                        "blob_name": <BLOB_NAME>,
                                        "expiration_time": <EXPIRATION_TIME>
                                    }
                    
            2. BAD_REQUEST - 400
                    Response-body : {
                                        "error" : <ERROR_DESCRIPTION>
                                    }
            3. SERVER_ERROR - 500
                    Response-body : {
                                        "error" : <ERROR_DESCRIPTION>
                                    }
'''
@app.route('/upload', methods=['GET'])
def get_upload_sas():
    try:
        sas_request_schema = SasRequestSchema()
        errors = sas_request_schema.validate(request.json)
        if errors:
            return jsonify({"error": errors}), 400
        else:
            container_name = request.json['container_name']
            blob_name = request.json['blob_name']
            expiration_time = datetime.now() + timedelta(minutes=config['azure_sas_expiration_time'])

            uri = upload_blob_sas(
                account_name=config['azure_storage_account_name'],
                account_key=config['azure_storage_account_key'],
                container_name=container_name,
                blob_name=blob_name,
                expiration_time=expiration_time
            )

            return jsonify({
                "uri": uri,
                "container_name": container_name,
                "blob_name": blob_name,
                "expiration_time": expiration_time
            })

    except Exception as ex:
        return jsonify({"error": str(ex)}), 500


'''
Generates a SAS for downloading a blob from a Container in Azure

 Endpoint: /download
 Method: Get
 Content-type: Application/json
 Request-body: { 
                    "container_name" : <CONTAINER_NAME>,
                    "blob_name" : <BLOB_NAME>
               }
 Response: 
            1. OK - 200
                    Response-body : {
                                        "uri": <URI>,
                                        "container_name": <CONTAINER_NAME>,
                                        "blob_name": <BLOB_NAME>,
                                        "expiration_time": <EXPIRATION_TIME>
                                    }

            2. BAD_REQUEST - 400
                    Response-body : {
                                        "error" : <ERROR_DESCRIPTION>
                                    }
            3. SERVER_ERROR - 500
                    Response-body : {
                                        "error" : <ERROR_DESCRIPTION>
                                    }
'''
@app.route('/download', methods=['GET'])
def get_download_sas():
    try:
        sas_request_schema = SasRequestSchema()
        errors = sas_request_schema.validate(request.json)
        if errors:
            return jsonify({"error": errors}), 400
        else:
            container_name = request.json['container_name']
            blob_name = request.json['blob_name']
            expiration_time = datetime.now() + timedelta(minutes=config['azure_sas_expiration_time'])

            uri = download_blob_sas(
                account_name=config['azure_storage_account_name'],
                account_key=config['azure_storage_account_key'],
                container_name=container_name,
                blob_name=blob_name,
                expiration_time=expiration_time
            )

            return jsonify({
                "uri": uri,
                "container_name": container_name,
                "blob_name": blob_name,
                "expiration_time": expiration_time
            })

    except Exception as ex:
        return jsonify({"error": str(ex)}), 500


'''
Lists the blobs in a container

 Endpoint: /list
 Method: Get
 Content-type: Application/json
 Request-body: { 
                    "container_name" : <CONTAINER_NAME>,
               }
 Response: 
            1. OK - 200
                    Response-body : [
                                        {
                                            "creation_time": <CREATION_TIME>,
                                            "last_modified": <LAST_MODIFIED_TIME>,
                                            "name": <FILE_NAME>,
                                            "size": <SIZE_IN_BYTES>
                                         },
                                         ....   
                                    ]

            2. BAD_REQUEST - 400
                    Response-body : {
                                        "error" : <ERROR_DESCRIPTION>
                                    }
            3. SERVER_ERROR - 500
                    Response-body : {
                                        "error" : <ERROR_DESCRIPTION>
                                    }
'''
@app.route('/list', methods=['GET'])
def list_blobs():
    try:
        list_request_schema = ListRequestSchema()
        errors = list_request_schema.validate(request.json)
        if errors:
            return jsonify({"error": errors}), 400
        else:
            container_name = request.json['container_name']
            res = ls(config["azure_storage_connectionstring"], container_name)
            return jsonify(res)
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500


'''
Delete a blob in a container

 Endpoint: /delete
 Method: Delete
 Content-type: Application/json
 Request-body: { 
                    "container_name" : <CONTAINER_NAME>,
                    "blob_name" : <BLOB_NAME>
               }
 Response: 
            1. OK - 200
                    Response-body : {
                                        "message": "Deleted"
                                     }

            2. BAD_REQUEST - 400
                    Response-body : {
                                        "error" : <ERROR_DESCRIPTION>
                                    }
            3. SERVER_ERROR - 500
                    Response-body : {
                                        "error" : <ERROR_DESCRIPTION>
                                    }
'''
@app.route('/delete', methods=['DELETE'])
def delete_blob():
    try:
        delete_request_schema = DeleteRequestSchema()
        errors = delete_request_schema.validate(request.json)
        if errors:
            return jsonify({"error": errors}), 400
        else:
            container_name = request.json['container_name']
            blob_name = request.json['blob_name']
            delete(config["azure_storage_connectionstring"], container_name, blob_name)
            return jsonify({
                "message": "Deleted"
            })
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500


@app.route('/upload', methods=['POST'])
def report_route_post():
    try:
        f = request.files['file']
        f.save("files/" + f.filename)
        resp = upload("files/" + f.filename, config["azure_storage_connectionstring"], config["images_container_name"],
                      True)
        if resp:
            return jsonify({"message": "Your upload request has been submitted"}), 200
        else:
            return jsonify({"error": "Something went wrong"}), 500
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500


if __name__ == '__main__':
    config = load_config()
    app.run(debug=True, port=5001)
    # resp = ls(config["azure_storage_connectionstring"], config["images_container_name"])
    # resp = upload("file_route", config["azure_storage_connectionstring"], config["images_container_name"], True)
    # resp = delete(config["azure_storage_connectionstring"], config["images_container_name"], "browser.svg")
    # resp = download(config["azure_storage_connectionstring"], config["images_container_name"], "GX_wallpaper_1920x1080.jpg")
    # print(resp)
