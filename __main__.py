# Info #
# PythonPublisher
# This script will create a web ui at http://localhost:3000/ to schedule updates.
# You can set the port by setting the PORT environment variable.
# You can also set the admin password by setting the adminPassword environment variable.
# Made by iamEvanYT (Github)

# Usage: python .

# CONFIG #
adminPassword = "password" # The password for the admin user in web panel.

# SCRIPT #
version = "v2.0.0"
from dotenv import load_dotenv
load_dotenv() # Load .env file

from flask import Flask, send_from_directory, jsonify, request, render_template
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import json
import uuid
import time
from threading import Thread
import update

def delete_file(file_path):
    try:
        os.remove(file_path)
        return True
    except OSError:
        return False

if os.environ.get('adminPassword') != None:
    adminPassword = str(os.environ.get('adminPassword'))

def read_json(file_path,defaultData):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return defaultData
    except Exception as e:
        return defaultData
def write_json(file_path, data):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        return True
    except Exception as e:
        return False

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 120 * 1000 * 1000 # 120MB max file size
app.static_url_path = ''
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'rbxl'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash(adminPassword),
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

@app.route('/')
@auth.login_required
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:filename>')
@auth.login_required
def serve_static(filename):
    if filename.endswith("/"):
        filename = filename[:-1]
    if os.path.isdir('static/' + filename):
        index_file = os.path.join(filename, 'index.html')
        if os.path.exists('static/' + index_file):
            return send_from_directory('static', index_file)
    return send_from_directory('static', filename)

def getScheduledUpdates():
    return read_json("./databases/scheduledUpdates.json", {})

def setScheduledUpdates(newJson):
    return write_json("./databases/scheduledUpdates.json", newJson)

def getSettings():
    configData = read_json("./databases/settings.json", {})
    if (configData.get("robloxCookie") == None):
        configData["robloxCookie"] = os.environ.get('robloxCookie','')
    if (configData.get("openCloudApiKey") == None):
        configData["openCloudApiKey"] = os.environ.get('openCloudApiKey','')
    return configData

def setSettings(newJson):
    if (os.environ.get('robloxCookie') and newJson.get("robloxCookie") == os.environ.get('robloxCookie')):
        del newJson["robloxCookie"]
    if (os.environ.get('openCloudApiKey') and newJson.get("openCloudApiKey") == os.environ.get('openCloudApiKey')):
        del newJson["openCloudApiKey"]
    if (newJson.get("robloxCookie") == ""):
        del newJson["robloxCookie"]
    if (newJson.get("openCloudApiKey") == ""):
        del newJson["openCloudApiKey"]
    return write_json("./databases/settings.json", newJson)

# API endpoint to retrieve scheduled updates
@app.route('/api/getscheduledupdates', methods=['GET'])
@auth.login_required
def get_scheduled_updates():
    return jsonify(getScheduledUpdates())

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def toInt(num):
    try:
        return int(num)
    except:
        return 0

# API endpoint to create a new update
@app.route('/api/setnewupdate', methods=['POST'])
@auth.login_required
def set_new_update():
    # Generate a unique ID for the new update
    UID = uuid.uuid4().hex
    gameFile = request.files.get("file")
    fileSize = gameFile.seek(0, os.SEEK_END)
    gameFile.seek(0, os.SEEK_SET)
    print("fileSize",fileSize)
    if fileSize > (100 * 1000 * 1000): # 100MB max file size
       return jsonify({"message": "This RBXL file is too big!"}) 
    
    formData = request.form.to_dict()
    newScheduledUpdate = {
        "id": UID,
        "updateTime": toInt(formData.get("updateTime")),
        "universeId": toInt(formData.get("universeId","0")),
        "placeId": toInt(formData.get("placeId","0")),
        "restartServers": formData.get("restartServers","none"),
        "updateName": formData.get("updateName","Unnamed Update"),
        "updateType": formData.get("updateType","publish"),
        "overrideCookie": formData.get("overrideCookie",""),
        "overrideOpenCloudKey": formData.get("overrideOpenCloudKey",""),
        "status": "Scheduled",
        "messagingServiceTopic": formData.get("messagingServiceTopic","")
    }
    if newScheduledUpdate["updateName"] == "":
        newScheduledUpdate["updateName"] = "Unnamed Update"
    if newScheduledUpdate["universeId"] == 0 or newScheduledUpdate["placeId"] == 0:
        return jsonify({"message": "You must specify a universe ID or place ID"})
    if gameFile and allowed_file(gameFile.filename):
        filename = UID + ".rbxl"
        gameFile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        return jsonify({"message": "You must upload a valid .rbxl file"})
    updates = getScheduledUpdates()
    updates[UID] = newScheduledUpdate
    setScheduledUpdates(updates)
    return jsonify({"message": "New update scheduled successfully"})

@app.route('/api/updatescheduledupdate', methods=['POST'])
@auth.login_required
def update_an_update():
    updatesToSearch = getScheduledUpdates()
    json = request.get_json()
    update = updatesToSearch.get(json.get("id",""))
    if update == None:
        return jsonify({"message": "Update not found"})
    if json.get("updateName"):
        update["updateName"] = json.get("updateName")
    if json.get("updateTime"):
        update["updateTime"] = toInt(json.get("updateTime"))
    if json.get("universeId"):
        update["universeId"] = toInt(json.get("universeId"))
    if json.get("placeId"):
        update["placeId"] = toInt(json.get("placeId"))
    if json.get("restartServers"):
        update["restartServers"] = json.get("restartServers")
    if json.get("updateType"):
        update["updateType"] = json.get("updateType")
    if update["updateName"] == "":
        update["updateName"] = "Unnamed Update"
    if update["universeId"] == 0 or update["placeId"] == 0:
        return jsonify({"message": "You must specify a universe ID or place ID"})
    updates = getScheduledUpdates()
    updates[update["id"]] = update
    setScheduledUpdates(updates)
    return jsonify({"message": "Editted scheduled update successfully"})

@app.route('/api/deletescheduledupdate', methods=['DELETE'])
@auth.login_required
def delete_scheduled_update():
    updatesToSearch = getScheduledUpdates()
    json = request.get_json()
    update = updatesToSearch.get(json.get("id",""))
    if update == None:
        return jsonify({"message": "Update not found"})
    updates = getScheduledUpdates()
    del updates[update["id"]]
    setScheduledUpdates(updates)
    delete_file("./uploads/{UID}.rbxl".format(UID=update["id"]))
    return jsonify({"message": "Scheduled update deleted successfully"})

# API endpoint to get settings
@app.route('/api/getsettings', methods=['GET'])
@auth.login_required
def get_settings():
    return jsonify(getSettings())

# API endpoint to update settings
@app.route('/api/setsettings', methods=['POST'])
@auth.login_required
def set_settings():
    updated_settings = request.get_json()
    setSettings(updated_settings)
    return jsonify({"message": "Settings updated successfully"})

print("PythonPublisher started!")
print(f"Version: {version}")
print("Created by iamEvanYT (Github)")
    
def UpdateGame(UID,placeFilePath,openCloudApiKey,universeId,placeId,versionType,robloxCookie,shouldReplaceServers,successfulPublishEventName,timeToRun):
    success = update.RunUpdate(placeFilePath,openCloudApiKey,universeId,placeId,versionType,robloxCookie,shouldReplaceServers,successfulPublishEventName,timeToRun)
    get = getScheduledUpdates()
    if success == True:
        get[UID]["status"] = "Completed"
    else:
        get[UID]["status"] = "Failed"
    setScheduledUpdates(get)
    
pathTemplate = "./uploads/{fileId}.rbxl"
def CheckScheduledTasks():
    updates = getScheduledUpdates()
    for id in updates:
        update = updates[id]
        # check if epoch update time is less than current epoch time
        # Start task 2 seconds before the timeToRun, because of the time it takes to publish the place file + shutting down servers
        if ((update["updateTime"]-2) <= int(time.time()) and update["status"] == "Scheduled"):
            get = getScheduledUpdates() # lock the task first so no other loops can run it
            get[id]["status"] = "Working"
            setScheduledUpdates(get)
            filePath = pathTemplate.format(fileId=id)
            settings = getSettings()
            openCloudApiKey = settings["openCloudApiKey"]
            universeId = update["universeId"]
            placeId = update["placeId"]
            if update["updateType"] == "publish":
                versionType = "Published"
            else:
                versionType = "Saved"
            robloxCookie = settings["robloxCookie"]
            if update["overrideCookie"] != "":
                robloxCookie = update["overrideCookie"]
            if update["overrideOpenCloudKey"] != "":
                openCloudApiKey = update["overrideOpenCloudKey"]
            shouldReplaceServers = False
            if update["restartServers"] == "shutdown":
                shouldReplaceServers = False
            elif update["restartServers"] == "migrate":
                shouldReplaceServers = True
            else:
                robloxCookie = ""
            successfulPublishEventName = ""
            if update["messagingServiceTopic"] != "":
                successfulPublishEventName = update["messagingServiceTopic"]
            timeToRun = update["updateTime"]
            updateThread = Thread(target=UpdateGame, args=(id,filePath,openCloudApiKey,universeId,placeId,versionType,robloxCookie,shouldReplaceServers,successfulPublishEventName,timeToRun))
            updateThread.start()
           
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403
           
def RunFlask():
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 3000), debug=False)

flaskRun = Thread(target=RunFlask)
flaskRun.daemon = True
flaskRun.start()

def CheckScheduledTasksAsync():
    try:
        while True:
            CheckScheduledTasks()
            time.sleep(0.5)  # Sleep for a short duration to avoid high CPU usage
    except KeyboardInterrupt:
        exit(0)

CheckScheduledTasksAsync()