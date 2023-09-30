
// REFERENCES: 
// https://github.com/OtchereDev/yt_movie_booking_website/blob/main/static/backend.js
// https://www.youtube.com/watch?v=yKB7PNggRo8&list=PLj96HqfVI_3r28IFry8s-GLTyRhLlqKRS

const cta_btn = document.querySelector('button.book-btn');

async function contactAPI(url, body) {
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
    })
    return response.json()
}

// function convertTimeto convert time from "5 p.m." or "5:40 p.m." to "17:00:00" or "17:40:00"
function convertTime(time) {
    // match the time string and extract the hour, minute and am/pm
    // index 0 is the full match, index 1 is the hour, index 2 is the minute and index 3 is the am/pm
    // the regex looks for 1 or 2 digits followed by a colon followed by 2 digits followed by a space followed by 1 or 2 letters followed by a period
    // the i at the end makes the regex case insensitive
    // the ? after the colon makes the minute part optional
    // the ? after the space makes the space part optional
    // the ? after the letters makes the letters part optional
    // the ? after the . makes the . part optional
    let hour, minute, ampm;
    if (time.toLowerCase() === 'noon') {
        hour = 12;
        minute = 0;
        ampm = 'p.m.';
    } else if (time.toLowerCase() === 'midnight') {
        hour = 0;
        minute = 0;
        ampm = 'a.m.';
    } else {
        [, hour, minute, ampm] = time.match(/^(\d{1,2})(?::(\d{2}))?\s+([ap]\.m\.)/i);
    }
    let hourInt = parseInt(hour);
    if (ampm.toLowerCase() === 'p.m.' && hourInt !== 12) {
        hourInt += 12;
    } else if (ampm.toLowerCase() === 'a.m.' && hourInt === 12) {
        hourInt = 0;
    }
    const paddedHour = hourInt.toString().padStart(2, '0');
    const paddedMinute = (minute || '00').padStart(2, '0');
    return `${paddedHour}:${paddedMinute}:00`;
}

start_time = convertTime(start_time);
end_time = convertTime(end_time);

const room_id = roomSelect.options[roomSelect.selectedIndex].value

contactAPI("/showseats", { room_id }).then(data => {
    const numRows = data["numRows"]
    const numSeats = data["numSeats"]
    const capacity = data["capacity"]

    let room_cap = document.getElementById("capacity-display").innerHTML = "This room's capacity is " + capacity + ".";
    
    // for every row, create a div with class row
    for (let i = 0; i < numRows; i++) {
        const row = document.createElement("div")
        row.classList.add("row")
        row.id = "seatmap-row"
        // for every seat in the row, create a div with class seat
        for (let j = 0; j < numSeats; j++) {
            const seat = document.createElement("div")
            seat.classList.add("seat")
            row.appendChild(seat)
        }
        document.querySelector(".container").appendChild(row)
    }
})

// format date from Feb 1, 2021 to 2021-02-01
const formattedDate = date.split(" ").reverse().join("-")

const combinedStartTime = `${formattedDate} ${start_time}`;

const combinedEndTime = `${formattedDate} ${end_time}`;

// contact the API to get the seats that are occupied and pass the room_id and the start_time and end_time
contactAPI("/occupied/", { room_id, combinedStartTime, combinedEndTime }).then(data => {
    // store all seats unoccupied in a variable
    const all_seats = document.querySelectorAll(".seat:not(.occupied)")

    const occupied_seat = data["occupied_seats"]
    const room_id = data["room"]

    const seat_LocalStorage = localStorage.getItem("selectedSeats") ? JSON.parse(localStorage.getItem("selectedSeats")) : null
    const room_index = localStorage.getItem("selectedRoomIndex")

    const LS_room = roomSelect.options[room_index].textContent

    if (LS_room == room_id) {
        if (occupied_seat !== null && occupied_seat.length > 0) {
            all_seats.forEach((seat, index) => {
                if (occupied_seat.indexOf(index) > -1) {
                    seat.classList.add('occupied');
                    seat.classList.remove('selected');
                }
            })
        }

        if (seat_LocalStorage !== null) {
            seat_LocalStorage.forEach((seat, index) => {

                if (occupied_seat.includes(seat)) {
                    seat.localStorage.splice(index, 1);
                    localStorage.setItem("selectedSeats", seat_LocalStorage);
                }
            });
        }
    }
    updateSelectedCount();
})

cta_btn.addEventListener('click', e => {

    const room_id = roomSelect.options[roomSelect.selectedIndex].value
    const seat_list = JSON.parse(localStorage.getItem("selectedSeats"))


    if (seat_list !== null && seat_list.length > 0) {
        // get the first item in the seat_list and increase it by 1
        const seat = seat_list[0] + 1

        data = {
            room_id,
            seat,
            date,
            start_time,
            end_time
        }
        const url = "/addbasket/" + room_id + "/" + seat + "/" + date + "/" + start_time + "/" + end_time

        window.location.href = url
    }
})
