# Info #
# PythonPublisher
# This script will publish a place file to a Roblox experience at a specific set time.
# Made by iamEvanYT (Github)

# SCRIPT #
import requests
import time
import os
import sys
import json
hasRan = False
version = "v1.1.1"

def check_file_exists(file_path):
    return os.path.exists(file_path)


def delete_file(file_path):
    try:
        os.remove(file_path)
        return True
    except OSError:
        return False

def RunUpdate(placeFilePath,openCloudApiKey,universeId,placeId,versionType,robloxCookie,shouldReplaceServers,successfulPublishEventName,timeToRun):
    if check_file_exists(placeFilePath) == False:
        return False,"The place file does not exist."
    if (placeFilePath == "") or (placeFilePath == None):
        return False,"Please specify a place file path."

    if (openCloudApiKey == "") or (openCloudApiKey == None):
        return False, "Please specify an Open Cloud API key."

    if (universeId == 0) or (universeId == None):
        return False,"Please specify a universe ID."

    if (placeId == 0) or (placeId == None):
        return False,"Please specify a place ID."

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
        delete_file(placeFilePath)
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

        url = shutdownBaseUrl.format(placeId=placeId, shouldReplaceInstances=shouldReplaceServers)
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
            return False
        else:
            if versionType == "Published":
                print("Successfully published place!")
            else:
                print("Successfully saved place!")
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
            return True
                
    success = RunFunction()
    return success