import os
import yaml
from flask import Flask
from flask import request, jsonify
from ls import ls
from upload import upload
from delete import delete

app = Flask(__name__)


def load_config():
    dir_root = os.path.dirname(os.path.abspath(__file__))
    with open(dir_root + "/config.yaml", "r") as yamlfile:
        return yaml.load(yamlfile, Loader=yaml.FullLoader)


@app.route('/reports', methods=['GET'])
def ls_route_get():
    # noinspection PyBroadException
    try:
        res = ls(config["azure_storage_connectionstring"], config["images_container_name"])
        return jsonify(res), 200
    except Exception:
        return jsonify({"error": "Something went wrong"}), 500


@app.route('/report', methods=['POST'])
def report_route_post():
    # noinspection PyBroadException
    try:
        f = request.files['file']
        f.save("files/" + f.filename)
        resp = upload("files/" + f.filename, config["azure_storage_connectionstring"], config["images_container_name"], True)
        if resp:
            return jsonify({"message": "Your upload request has been submitted"}), 200
        else:
            return jsonify({"error": "Something went wrong"}), 500
    except Exception:
        return jsonify({"error": "Something went wrong"}), 500






if __name__ == '__main__':
    config = load_config()
    app.run(debug=True, port=5001)
    # resp = ls(config["azure_storage_connectionstring"], config["images_container_name"])
    # resp = upload("file_route", config["azure_storage_connectionstring"], config["images_container_name"], True)
    # resp = delete(config["azure_storage_connectionstring"], config["images_container_name"], "browser.svg")
    # resp = download(config["azure_storage_connectionstring"], config["images_container_name"], "GX_wallpaper_1920x1080.jpg")
    # print(resp)
