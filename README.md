# [PythonPublisher](https://github.com/iamEvanYT/PythonPublisher)
## Made by [iamEvanYT](https://github.com/iamEvanYT)

PythonPublisher is a Python script for automating the process of publishing Roblox places. It allows you to schedule the publish at a specific time, replace servers, and optionally restart servers if you provide a Roblox cookie. The script also provides flexibility by allowing configuration through environment variables or direct input.

Version 2 introduced a web panel to help schedule updates!

## Downloading the script
1. Download the whole repository as a `.zip` file
2. Uncompress it
3. Download python if you haven't

## Dependencies

Install all the dependencies using `pip install -r requirements.txt`

## Configuration

The following parameters are able to configure in the script:

- `adminPassword`: Password for logging into web admin panel.

The following parameters are able to configure in `.env` file:

- `adminPassword`: If specified, it will override the value configured inside the script.

- `openCloudApiKey`: Your Roblox Open Cloud API key, used for saving/publishing the place file & firing events through MessagingService. Generate one [here](https://create.roblox.com/dashboard/credentials).

- `robloxCookie`: Your Roblox Cookie, used for restarting servers. Leave blank to specify inside web panel.

- `PORT`: Specify a port. The default port is 3000.

## Running the Script

Command line Usage: `python .`<br>
Windows: Go inside the unzipped folder, and open `__main__.py`

Go to http://localhost:3000 or `localhost:<PORT>` if you have changed it in .env
<br>Login using Username `admin` and your set password.<br>
Default Password is `password`.

The panel will be online until either `Ctrl+C` is used in Command Prompt or the file is closed in Windows.

## Contributions

This script is developed by [iamEvanYT](https://github.com/iamEvanYT). Contributions are welcomed via GitHub issues and pull requests.

## License

This project is licensed under the MIT License.

## Disclaimer

Use this script responsibly. The developers of this script are not responsible for any misuse or violation of Roblox's Terms of Service. Always respect Roblox's rules when using this script.

This script is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the script or the use or other dealings in the script.