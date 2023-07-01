# Info #
# PythonPublisher
# This script will publish a place file to a Roblox experience at a specific set time.
# Made by iamEvanYT (Github)

# Usage: python main.py [timeToRun] [universeId] [placeId] [placeFilePath] [versionType] [openCloudApiKey] [robloxCookie] [shouldReplaceServers] [successfulPublishEventName]

# CONFIG #
useEnv = False # If enabled, use values from .env file instead of the values below. (Better security, if universeId is defined in .env, the value below will be ignored)
useSys = True # If enabled and value is passed in command line, use values from command line instead of the values below.
timeToRun = 0 #T his is a timestamp (https://www.epochconverter.com/)
universeId = 0 # The identifier of the experience in which you want to publish your place to. You can copy your experience's Universe ID on Creator Dashboard.
placeId = 0 # The identifier of the place you want to publish. You can copy your place's Place ID on Creator Dashboard.
versionType = "Published" # The version type of the place you want to publish. You can choose between "Published" and "Saved".
openCloudApiKey = "" # Your Roblox Open Cloud API key, used for saving/publishing the place file. (Generate one here: https://create.roblox.com/dashboard/credentials)
robloxCookie = "" # Your Roblox Cookie, used for restarting servers. (Leave blank to disable, servers with only be restarted if the new version is Published)
placeFilePath = "./place.rbxl" # The Path of the Roblox place file (RBXL Format) you want to publish.
shouldReplaceServers = False # Whether or not you want to replace servers instead of restarting them. (Buggy & Experimental) (Not recommended)
successfulPublishEventName = "" # The name of the MessagingService event that will be fired when the place is successfully published. (Leave blank to disable)

# SCRIPT #
import requests
import time
import os
import sys
import json
hasRan = False
version = "v1.1.1"

if (useEnv == True) or (os.environ.get('universeId') != None):
    # Use default values if not defined in .env file
    if os.environ.get('useSys') != None:
        useSys = bool(os.environ.get('useSys'))
    if os.environ.get('timeToRun') != None:
        timeToRun = float(os.environ.get('timeToRun'))
    if os.environ.get('universeId') != None:
        universeId = int(os.environ.get('universeId'))
    if os.environ.get('placeId') != None:
        placeId = int(os.environ.get('placeId'))
    if os.environ.get('versionType') != None:
        versionType = str(os.environ.get('versionType'))
    if os.environ.get('openCloudApiKey') != None:
        openCloudApiKey = str(os.environ.get('openCloudApiKey'))
    if os.environ.get('robloxCookie') != None:
        robloxCookie = str(os.environ.get('robloxCookie'))
    if os.environ.get('placeFilePath') != None:
        placeFilePath = str(os.environ.get('placeFilePath'))
    if os.environ.get('shouldReplaceServers') != None:
        shouldReplaceServers = bool(os.environ.get('shouldReplaceServers'))
    if os.environ.get('successfulPublishEventName') != None:
        successfulPublishEventName = str(os.environ.get('successfulPublishEventName'))

if (useSys == True) and (len(sys.argv) > 1):
    try:
        if (sys.argv[1] != None):
            timeToRun = int(sys.argv[1])
        if (sys.argv[2] != None):
            universeId = int(sys.argv[2])
        if (sys.argv[3] != None):
            placeId = int(sys.argv[3])
        if (sys.argv[4] != None):
            placeFilePath = sys.argv[4]
        if (sys.argv[5] != None):
            versionType = sys.argv[5]
        if (sys.argv[6] != None):
            openCloudApiKey = sys.argv[6]
        if (sys.argv[7] != None):
            robloxCookie = sys.argv[7]
        if (sys.argv[8] != None):
            shouldReplaceServers = bool(sys.argv[8])
        if (sys.argv[9] != None):
            successfulPublishEventName = sys.argv[9]
    except:
        pass
    
if (placeFilePath == "") or (placeFilePath == None):
    raise Exception("Please specify a place file path.")

if (openCloudApiKey == "") or (openCloudApiKey == None):
    raise Exception("Please specify an Open Cloud API key.")

if (universeId == 0) or (universeId == None):
    raise Exception("Please specify a universe ID.")

if (placeId == 0) or (placeId == None):
    raise Exception("Please specify a place ID.")

desiredTimeToSave = (timeToRun - 2) # Start task 1 second before the timeToRun, because of the time it takes to publish the place file + shutting down servers
desiredTimeToShutdown = (timeToRun)

publishBaseUrl = "https://apis.roblox.com/universes/v1/{universeId}/places/{placeId}/versions?versionType={versionType}"
shutdownBaseUrl = "https://www.roblox.com/games/shutdown-all-instances?placeId={placeId}&replaceInstances={shouldReplaceInstances}"
messagingServiceBaseUrl = "https://apis.roblox.com/messaging-service/v1/universes/{universeId}/topics/{topic}"
def SetPlaceFile():
    url = publishBaseUrl.format(universeId=universeId, placeId=placeId, versionType=versionType)
    # Post the file
    with open(placeFilePath, 'rb') as file:
        response = requests.post(url, data=file, headers={
            "x-api-key": openCloudApiKey,
            "Content-Type": "application/octet-stream"
        })
    if response.status_code == 200:
        try:
            json_response = response.json()
            if isinstance(json_response, dict) and json_response.get("versionNumber"):
                return True, "The response is a JSON object and it contains the key 'versionNumber'"
            else:
                return False, ("The response is a JSON object, but it does not contain the key 'versionNumber'")
        except ValueError:
            return False, "The response is not a JSON object"
    else:
        return False, ("Request failed with status code:"+ str(response.status_code))
        
def GetAuthenticatedSession():
    session = requests.Session()
    session.cookies[".ROBLOSECURITY"] = str(robloxCookie)
    session.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    }

    # send first request
    req = session.post(
        url="https://auth.roblox.com/"
    )
    
    if "X-CSRF-Token" in req.headers:  # check if token is in response headers
        session.headers["X-CSRF-Token"] = req.headers["X-CSRF-Token"]  # store the response header in the session
    return session
        
def ShutdownServers():
    session = GetAuthenticatedSession()

    url = shutdownBaseUrl.format(placeId=placeId, shouldReplaceInstances=True)
    response = session.post(url, data={
        "placeId": placeId,
        "replaceInstances": shouldReplaceServers
    })
    if response.status_code == 200:
        return True, "Successfully shutdown servers"
    else:
        return False, ("Request failed with status code:"+ str(response.status_code))

def FireMessagingServiceEvent():
    url = messagingServiceBaseUrl.format(universeId=universeId, topic=successfulPublishEventName)
    response = requests.post(url, headers={
        "x-api-key": openCloudApiKey,
        "Content-Type": "application/json"
    }, json={
        "message": placeId
    })
    if response.status_code == 200:
        return True, "Successfully fired event"
    else:
        return False, ("Request failed with status code:"+ str(response.status_code))

def RunFunction():
    status, message = SetPlaceFile()
    if status == False:
        print("Failed to publish place: " + message)
        return
    else:
        if versionType == "Published":
            print("Successfully published place!")
            if (robloxCookie != "") or (successfulPublishEventName != ""):
                while (time.time() < desiredTimeToShutdown):
                    time.sleep(0.2)
            if successfulPublishEventName != "":
                print("Publishing message with MessagingService...")
                fireStatus,fireMsg = FireMessagingServiceEvent()
                if fireStatus != True:
                    print("Failed to publish message: " + fireMsg)
                else:
                    print("Successfully published message!")
            if robloxCookie != "":
                print("Restarting servers...")
                shutdownStatus,shutdownMsg = ShutdownServers()
                if shutdownStatus != True:
                    print("Failed to restart servers: " + shutdownMsg)
                else:
                    print("Successfully restarted servers!")
        else:
            print("Successfully saved place!")

print("PythonPublisher started!")
print(f"Version: {version}")
print("Created by iamEvanYT (Github)")
while True:
    if hasRan == True:
        break
    if time.time() >= desiredTimeToSave:
        RunFunction()
        hasRan = True
    time.sleep(0.5)
    
print("PythonPublisher finished running!")
while True:
    time.sleep(60*60)