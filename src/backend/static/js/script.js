const container = document.querySelector('.container');
const seats = document.querySelectorAll('.row .seat:not(.occupied)');
const count = document.getElementById('count');
const roomSelect = document.getElementById('room');

populateUI();

// Save selected index and 
function setRoomData(roomIndex) {
    localStorage.setItem('selectedRoomIndex', roomIndex);
}

// Update count
function updateSelectedCount() {
    // selected seats in the room
    const selectedSeats = document.querySelectorAll('.row .seat.selected');

    // Get all the seats in the row
    const allSeats = document.querySelectorAll('.row .seat');

    // copy selected seats into array and map through array to get index of each seat
    const seatsIndex = [...selectedSeats].map(seat => [...allSeats].indexOf(seat));

    // save selected seats to localstorage 
    localStorage.setItem('selectedSeats', JSON.stringify(seatsIndex));

    // set the room select values
    setRoomData(roomSelect.selectedIndex, roomSelect.value);
}


// Get data from localstorage and populate UI
function populateUI() {
    // set selectedSeats to null
    localStorage.setItem('selectedSeats', JSON.stringify([]));
    
    // disable the cta button
    document.querySelector('button.book-btn').classList.add('disabled');

    const selectedSeats = JSON.parse(localStorage.getItem('selectedSeats'));

    if (selectedSeats !== null && selectedSeats.length > 0) {
        seats.forEach((seat, index) => {
            if (selectedSeats.indexOf(index) > -1) {
                seat.classList.add('selected');
            }
        });
    }

    const selectedRoomIndex = localStorage.getItem('selectedRoomIndex');

    if (selectedRoomIndex !== null) {
        roomSelect.selectedIndex = selectedRoomIndex;
    }
}

//  select event
roomSelect.addEventListener('change', e => {
    setRoomData(e.target.selectedIndex, e.target.value);
    updateSelectedCount();
    // set selectedSeats to null
    localStorage.setItem('selectedSeats', JSON.stringify([]));
    // reload the page
    location.reload();
});

let numSelected = 0;

// Seat click event
if (container) {
    container.addEventListener('click', e => {
        if (
            // if the seat is not occupied and not selected
            e.target.classList.contains('seat') &&
            !e.target.classList.contains('occupied')
        ) {
            // enable the cta button
            document.querySelector('button.book-btn').classList.remove('disabled');
            // deselect current selected seat if there is one
            const currentSelected = document.querySelector('.selected');
            if (currentSelected) {
                currentSelected.classList.remove('selected');
            }
            e.target.classList.add('selected');
            updateSelectedCount();
        } else if (
            e.target.classList.contains('seat') && e.target.classList.contains('selected')
        ) {
            e.target.classList.remove('selected');
            updateSelectedCount();
        }
    });
}

// Initial count set
updateSelectedCount();
