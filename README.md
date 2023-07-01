# [PythonPublisher](https://github.com/iamEvanYT/PythonPublisher)
## Made by [iamEvanYT](https://github.com/iamEvanYT)

PythonPublisher is a Python script for automating the process of publishing Roblox places. It allows you to schedule the publish at a specific time, replace servers, and optionally restart servers if you provide a Roblox cookie. The script also provides flexibility by allowing configuration through environment variables or direct input.

## Configuration

The following parameters are used for configuring the script:

- `useSys`: If disabled, it will ignore values given from command line.

- `useEnv`: If enabled, use values from `.env` file instead of the values below. This offers better security. If `universeId` is defined in `.env`, the value in the script will be ignored and `.env` will be used.

- `timeToRun`: This is the time that this script will update your place. Get a timestamp [here](https://www.epochconverter.com/).

- `universeId`: The identifier of the experience in which you want to publish your place to. You can copy your experience's Universe ID on Creator Dashboard.

- `placeId`: The identifier of the place you want to publish. You can copy your place's Place ID on Creator Dashboard.

- `versionType`: The version type of the place you want to publish. You can choose between "Published" and "Saved".

- `openCloudApiKey`: Your Roblox Open Cloud API key, used for saving/publishing the place file. Generate one [here](https://create.roblox.com/dashboard/credentials).

- `robloxCookie`: Your Roblox Cookie, used for restarting servers. Leave blank to disable; servers will only be restarted if the new version is Published.

- `placeFilePath`: The path of the Roblox place file (RBXL Format) you want to publish.

- `shouldReplaceServers`: Whether or not you want to replace servers instead of restarting them. This feature is experimental and may be buggy, so it is not recommended.

## Running the Script

The script runs in an infinite loop (with `time.sleep` to pause execution) until the specified time to run is reached (`timeToRun`), at which point it calls the internal function `RunFunction()`. `RunFunction()` handles the process of publishing the place and optionally restarting servers.

To run the script, simply run `python .` in your terminal after cloning the Github Project.

Usage: `python . [timeToRun] [universeId] [placeId] [placeFilePath] [versionType] [openCloudApiKey] [robloxCookie] [shouldReplaceServers] [successfulPublishEventName]`

## Contributions

This script is developed by [iamEvanYT](https://github.com/iamEvanYT). Contributions are welcomed via GitHub issues and pull requests.

## License

This project is licensed under the MIT License.

## Disclaimer

Use this script responsibly. The developers of this script are not responsible for any misuse or violation of Roblox's Terms of Service. Always respect Roblox's rules when using this script.

This script is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the script or the use or other dealings in the script.