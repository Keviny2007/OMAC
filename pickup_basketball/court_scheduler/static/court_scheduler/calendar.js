document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/get-available-slots')
        .then(response => response.json())
        .then(slots => {
            const calendar = document.getElementById('calendar');
            slots.forEach(slot => {
                const slotDiv = document.createElement('div');
                slotDiv.textContent = `Court ${slot.court_number}: ${new Date(slot.start_time).toLocaleTimeString()} - ${new Date(slot.end_time).toLocaleTimeString()}`;
                slotDiv.className = 'time-slot';
                slotDiv.addEventListener('click', () => signUpForSlot(slot.id));
                calendar.appendChild(slotDiv);
            });
        });
});

function signUpForSlot(slotId) {
    const userName = localStorage.getItem('userName');
    fetch('/api/register-for-slot/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ name: userName, slot_id: slotId }),
    }).then(response => response.json())
      .then(data => {
          if (data.status === 'success') {
              alert('You have signed up successfully!');
              location.reload();  // Refresh the calendar
          }
      });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
