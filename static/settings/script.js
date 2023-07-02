// Make a GET request to fetch the settings from the server
fetch('/api/getsettings')
  .then(response => response.json())
  .then(data => {
    // Update the settings form fields with the fetched values
    document.getElementById('roblox-cookie').value = data.robloxCookie;
    document.getElementById('opencloud-api-key').value = data.openCloudApiKey;
  })
  .catch(error => {
    console.error('Error fetching settings:', error);
  });

// Get the form element
const form = document.querySelector('form');

// Add a submit event listener to the form
form.addEventListener('submit', event => {
  event.preventDefault();

  // Get the form values
  const robloxCookie = document.getElementById('roblox-cookie').value;
  const openCloudApiKey = document.getElementById('opencloud-api-key').value;

  // Create the payload object
  const payload = {
    robloxCookie,
    openCloudApiKey,
  };

  // Make a POST request to update the settings
  fetch('/api/setsettings', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  })
    .then(response => {
      if (response.ok) {
        // Settings update was successful
        alert('Settings updated successfully');
      } else {
        // Settings update failed
        alert('Failed to update settings');
      }
    })
    .catch(error => {
      alert('Error updating settings:', error);
    });
});
