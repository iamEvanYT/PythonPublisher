// Utility function to open the inspect modal
function openInspectModal(update) {
  const modal = document.getElementById('inspect-modal');
  const closeBtn = modal.querySelector('.close');
  const updateName = modal.querySelector('#inspect-update-name');
  const updateTime = modal.querySelector('#inspect-update-time');
  const updateUniverse = modal.querySelector('#inspect-update-universe');
  const updatePlace = modal.querySelector('#inspect-update-place');
  const updateRestart = modal.querySelector('#inspect-update-restart');
  const updateType = modal.querySelector('#inspect-update-type');
  const editButton = modal.querySelector('.edit-button');
  const deleteButton = modal.querySelector('.delete-button');

  // Update the modal content with the selected update details
  updateName.textContent = update.updateName;
  updateTime.textContent = new Date(update.updateTime * 1000).toLocaleString();
  updateUniverse.textContent = update.universeId;
  updatePlace.textContent = update.placeId;

  if (update.restartServers == "shutdown") {
    updateRestart.textContent = "Shutdown";
  } else {
    if (update.restartServers == "migrate") {
      updateRestart.textContent = "Migrate to latest version";
    } else {
      updateRestart.textContent = "None";
    }
  }

  if (update.updateType == "publish") {
    updateType.textContent = "Publish";
  } else {
    updateType.textContent = "Save";
  }

  // Set event listeners for edit and delete buttons
  editButton.addEventListener('click', () => {
    openEditModal(update);
  });

  deleteButton.addEventListener('click', () => {
    // Perform delete functionality for the selected update
    console.log('Delete button clicked for update:', update);
    // Remove the update from the list
    fetch(`/api/deletescheduledupdate`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ id: update.id }),
    })
      .then(response => {
        if (response.ok) {
          // Update was successful, show responseJson.message
          response.json().then(responseJson => {
            alert(responseJson.message);
          });
        } else {
          // Update failed
          response.json().then(responseJson => {
            alert(responseJson.message);
          });
        }
      }
      );
  });

  // Open the modal
  modal.style.display = 'block';

  // Close the modal when the close button is clicked
  closeBtn.addEventListener('click', () => {
    modal.style.display = 'none';
  });

  // Close the modal when the user clicks outside the modal content
  window.addEventListener('click', event => {
    if (event.target == modal) {
      modal.style.display = 'none';
    }
  });
}

// Utility function to open the edit modal
function openEditModal(update) {
  const modal = document.getElementById('edit-modal');
  const closeBtn = modal.querySelector('.close');
  const editForm = modal.querySelector('#edit-form');
  const updateNameInput = modal.querySelector('#edit-update-name');
  const updateTimeInput = modal.querySelector('#edit-update-time');
  const updateUniverseInput = modal.querySelector('#edit-update-universe');
  const updatePlaceInput = modal.querySelector('#edit-update-place');
  const updateRestartInput = modal.querySelector('#edit-update-restart');
  const updateTypeInput = modal.querySelector('#edit-update-type');

  // Set the current update values in the edit form
  updateNameInput.value = update.updateName;
  const currentDate = new Date(update.updateTime * 1000)
  // Get the individual components
  var year = currentDate.getFullYear();
  var month = (currentDate.getMonth() + 1).toString().padStart(2, '0');
  var day = currentDate.getDate().toString().padStart(2, '0');
  var hours = currentDate.getHours().toString().padStart(2, '0');
  var minutes = currentDate.getMinutes().toString().padStart(2, '0');

  // Format the components as a string in the datetime-local format
  var datetimeLocal = year + '-' + month + '-' + day + 'T' + hours + ':' + minutes;
  updateTimeInput.value = datetimeLocal;
  updateUniverseInput.value = update.universeId;
  updatePlaceInput.value = update.placeId;
  updateRestartInput.value = update.restartServers;
  updateTypeInput.value = update.updateType;

  // Handle form submission
  editForm.addEventListener('submit', event => {
    event.preventDefault();

    // Get the updated values from the form
    const updatedName = updateNameInput.value;
    const updatedTime = updateTimeInput.value;
    const updatedUniverse = updateUniverseInput.value;
    const updatedPlace = updatePlaceInput.value;
    const updatedRestart = updateRestartInput.value;
    const updatedType = updateTypeInput.value;

    const updateDateTime = new Date(updatedTime);
    const unixTimestamp = Math.floor(updateDateTime.getTime() / 1000); // Convert milliseconds to seconds

    // Send the updated data to the server using a POST request
    const payload = {
      id: update.id,
      updateName: updatedName,
      updateTime: unixTimestamp,
      universeId: updatedUniverse,
      placeId: updatedPlace,
      restartServers: updatedRestart,
      updateType: updatedType
    };

    fetch('/api/updatescheduledupdate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })
      .then(response => {
        if (response.ok) {
          response.json().then(responseJson => {
            alert(responseJson.message);
          });
          console.log('Update sent successfully');
        } else {
          console.error('Failed to send update');
        }
      })
      .catch(error => {
        console.error('Error sending update:', error);
      });

    // Close the modal
    modal.style.display = 'none';
    document.getElementById('inspect-modal').style.display = 'none';
  });

  // Open the modal
  modal.style.display = 'block';

  // Close the modal when the close button is clicked
  closeBtn.addEventListener('click', () => {
    modal.style.display = 'none';
  });

  // Close the modal when the user clicks outside the modal content
  window.addEventListener('click', event => {
    if (event.target == modal) {
      modal.style.display = 'none';
    }
  });
}

// Make a GET request to fetch the scheduled updates from the server
function FetchAllScheduledTasks() {
  fetch('/api/getscheduledupdates')
    .then(response => response.json())
    .then(data => {
      // Process the data and update the scheduled updates list
      const scheduledUpdatesList = document.querySelector('.scheduled-updates');
      scheduledUpdatesList.innerHTML = '';

      const updates = Object.values(data);
      updates.sort((a, b) => b.updateTime - a.updateTime);

      // Iterate over the scheduled updates and create list items
      updates.forEach(update => {
        const listItem = document.createElement('li');
        listItem.setAttribute('id', `update-${update.id}`);
        listItem.innerHTML = `
        <div class="update-info">
          <span class="update-name">${update.updateName}</span>
          <span class="update-time">${new Date(update.updateTime * 1000).toLocaleString()}</span>
          <span class="update-status">${update.status}</span>
        </div>
        <div class="update-actions">
          <button class="inspect-button">Inspect</button>
          <button class="edit-button">Edit</button>
          <button class="delete-button">Delete</button>
        </div>
      `;

        // Add event listeners to inspect, edit, and delete buttons
        const inspectButton = listItem.querySelector('.inspect-button');
        const editButton = listItem.querySelector('.edit-button');
        const deleteButton = listItem.querySelector('.delete-button');

        inspectButton.addEventListener('click', () => {
          openInspectModal(update);
        });

        editButton.addEventListener('click', () => {
          openEditModal(update);
        });

        deleteButton.addEventListener('click', () => {
          // Perform delete functionality or show confirmation dialog
          // Remove the update from the list
          fetch(`/api/deletescheduledupdate`, {
            method: 'DELETE',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id: update.id }),
          })
            .then(response => {
              if (response.ok) {
                // Update was successful, show responseJson.message
                response.json().then(responseJson => {
                  alert(responseJson.message);
                });
              } else {
                // Update failed
                response.json().then(responseJson => {
                  alert(responseJson.message);
                });
              }
            }
            );
        });

        // Set appropriate class for update status based on its value
        const updateStatusElement = listItem.querySelector('.update-status');
        if (update.status === 'Scheduled') {
          updateStatusElement.classList.add('status-pending');
        } else if (update.status === 'Completed') {
          updateStatusElement.classList.add('status-completed');
        } else if (update.status === 'Failed') {
          updateStatusElement.classList.add('status-failed');
        } else if (update.status === 'Working') {
          updateStatusElement.classList.add('status-working');
        }

        scheduledUpdatesList.appendChild(listItem);
      });
    })
    .catch(error => {
      console.error('Error fetching scheduled updates:', error);
    });
}

setInterval(FetchAllScheduledTasks, 1000);