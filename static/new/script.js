// Get the form element
const form = document.querySelector('form');

// Add a submit event listener to the form
form.addEventListener('submit', event => {
  event.preventDefault();

  // Get the form values
  const gameFileInput = document.getElementById('game-file');
  const gameFile = gameFileInput.files[0];
  const updateTime = document.getElementById('update-time').value;
  const universeId = document.getElementById('universe-id').value;
  const placeId = document.getElementById('place-id').value;
  const restartServers = document.getElementById('restart-servers').value;
  const updateName = document.getElementById('update-name').value;
  const updateType = document.getElementById('update-type').value;
  const overrideCookie = document.getElementById('override-roblox-cookie').value;
  const overrideOpenCloudKey = document.getElementById('override-opencloud-api-key').value;
  const messagingServiceTopic = document.getElementById('messaging-service-topic').value;

  if (updateTime == "") {
    alert('Please select a valid update time');
    return;
  }

  // Validate the file extension
  if (gameFile && gameFile.name.endsWith('.rbxl')) {
    const updateDateTime = new Date(updateTime);
    const unixTimestamp = Math.floor(updateDateTime.getTime() / 1000); // Convert milliseconds to seconds

    let formData = new FormData();

    formData.append('file', gameFile);
    formData.append('updateTime', unixTimestamp);
    formData.append('universeId', universeId);
    formData.append('placeId', placeId);
    formData.append('restartServers', restartServers);
    formData.append('updateName', updateName);
    formData.append('updateType', updateType);
    formData.append('overrideCookie', overrideCookie);
    formData.append('overrideOpenCloudKey', overrideOpenCloudKey);
    formData.append('messagingServiceTopic', messagingServiceTopic);

    // Make a POST request to create a new update
    fetch('/api/setnewupdate', {
      method: 'POST',
      body: formData,
    })
      .then(response => {
        if (response.ok) {
          // Update was successful, show responseJson.message
          response.json().then(responseJson => { 
            alert(responseJson.message);
            if (responseJson.message == "New update scheduled successfully") {
              // Redirect to the home page
              window.location.href = '/';
            }
          });
          // Reset the form fields
          form.reset();
        } else {
          // Update failed
          alert('Failed to schedule a new update');
        }
      })
      .catch(error => {
        alert('Error scheduling a new update:', error);
      });
  } else {
    alert('Please select a valid RBXL file');
  }
});