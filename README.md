# [PythonPublisher](https://github.com/iamEvanYT/PythonPublisher)
## Made by [iamEvanYT](https://github.com/iamEvanYT)

The `PythonPublisher` script is designed to publish a place file to a specific Roblox experience at a certain time. This is highly useful for Roblox developers who want to automate updates to their game, and is created by Github user `iamEvanYT`.

## Configuration

Firstly, there are a set of configurable variables that you need to set:

```py
# CONFIG #
useEnv = False #If enabled, use values from .env file instead of the values below. (Better security, if universeId is defined in .env, the value below will be ignored)
timeToRun = 0 #This is a timestamp (https://www.epochconverter.com/)
universeId = 0 #The identifier of the experience in which you want to publish your place to. You can copy your experience's Universe ID on Creator Dashboard.
placeId = 0 #The identifier of the place you want to publish. You can copy your place's Place ID on Creator Dashboard.
versionType = "Published" #The version type of the place you want to publish. You can choose between "Published" and "Saved".
openCloudApiKey = "" #Your Roblox Open Cloud API key, used for saving/publishing the place file. (Register one here: https://create.roblox.com/dashboard/credentials)
robloxCookie = "" #Your Roblox Cookie, used for restarting servers. (Leave blank to disable, servers with only be restarted if the new version is Published)
placeFilePath = "./place.rbxl" #The Path of the Roblox place file (RBXL Format) you want to publish.
shouldReplaceServers = False #Whether or not you want to replace servers instead of restarting them. (Buggy & Experimental) (Not recommended)
```

## Running the Script

The script begins by setting up some preliminary data, such as URLs for publishing and shutting down servers, and a check for the use of a `.env` file for storing configuration. 

After that, it defines several **internal** functions:

### `SetPlaceFile()`

This function is used to upload the place file to the Roblox server. It uses a `POST` request to the Roblox API with the place file as the payload. It will return the status of the operation and a corresponding message.

### `GetAuthenticatedSession()`

This function is used to create an authenticated session with Roblox. It sets the necessary headers and cookies for the session, and makes a request to get a CSRF token, which is then added to the session headers.

### `ShutdownServers()`

This function uses the authenticated session from `GetAuthenticatedSession()` to send a `POST` request to Roblox, telling it to shut down all instances of the specified place. The status of the operation and a corresponding message are returned.

### `RunFunction()`

This function calls `SetPlaceFile()` and then depending on the configuration, may also call `ShutdownServers()`.

The script then enters a loop, waiting until the desired publish time is reached. Once it is, it calls `RunFunction()`, prints a success message, and enters an idle state.

## Conclusion

`PythonPublisher` is a powerful tool for automating game updates on Roblox. By configuring the script properly, developers can save a lot of time and effort and update when they are offline.