# Info #
# Made by iamEvanYT (Github)

# CONFIG #
timeToRun = 0 #This is a timestamp (https://www.epochconverter.com/)
universeId = 0 #The identifier of the experience in which you want to publish your place to. You can copy your experience's Universe ID on Creator Dashboard.
placeId = 0 #The identifier of the place you want to publish. You can copy your place's Place ID on Creator Dashboard.
versionType = "Published" #The version type of the place you want to publish. You can choose between "Published" and "Saved".
openCloudApiKey = "" #Your Roblox Open Cloud API key, used for saving/publishing the place file. (Register one here: https://create.roblox.com/dashboard/credentials)
robloxCookie = "" #Your Roblox Cookie, used for restarting servers. (Leave blank to disable, servers with only be restarted if the new version is Published)
placeFilePath = "./place.rbxl" #The Path of the Roblox place file you want to publish.
shouldReplaceServers = False #Whether or not you want to replace servers instead of restarting them. (Buggy & Experimental) (Not recommended)

# SCRIPT #
import requests
import time
hasRan = False

desiredTime = (timeToRun - 1) # Start task 1 second before the timeToRun, because of the time it takes to publish the place file + shutting down servers

publishBaseUrl = "https://apis.roblox.com/universes/v1/{universeId}/places/{placeId}/versions?versionType={versionType}"
shutdownBaseUrl = "https://www.roblox.com/games/shutdown-all-instances?placeId={placeId}&replaceInstances={shouldReplaceInstances}"
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

def RunFunction():
    status, message = SetPlaceFile()
    if status == False:
        print("Failed to publish place: " + message)
        return
    else:
        if versionType == "Published":
            if robloxCookie != "":
                print("Successfully published place, restarting servers...")
                shutdownStatus,shutdownMsg = ShutdownServers()
                if shutdownStatus != True:
                    print("Failed to restart servers: " + shutdownMsg)
                else:
                    print("Successfully restarted servers!")
            else:
                print("Successfully published place!")
        else:
            print("Successfully saved place!")

print("Script started!")
while True:
    if hasRan == True:
        break
    if time.time() >= desiredTime:
        RunFunction()
        hasRan = True
    time.sleep(0.5)