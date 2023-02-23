// The button selected by the user to Verify the booking
const scan_btn = document.querySelector('span.scan-btn');

// get the booking id from the button's data attribute


// Function to get the details of the booking from the database given its ID
async function contactAPI(url, body) {
    console.log("Contacting API at " + url);

    const response = await fetch(url, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
    })
    return response.json()
}

// when the page loads, check if the booking has been verified
// contactAPI("/booking_details/" + booking_id).then(data => {
//     console.log("Booking id is: ");f
//     console.log(booking_id);
//     console.log("Booking data is: ");
//     console.log(data);
//     console.log("Booking verification status: ");
//     console.log(data.is_verified);

//     // if the booking has been verified, change the button text to "Verified"
//     if (data.is_verified) {
//         scan_btn.style.display = "none";
//         // show the verified paragraph
//         document.getElementById("verification-status").style.display = "block";
        
//     }
// });


// Event listener for the Verify button
scan_btn.addEventListener('click', e => {
    const booking_id = scan_btn.dataset.bkgid;
    console.log(booking_id);
    // use the booking ID to retrieve the booking from the database
    contactAPI("/booking_details/" + booking_id).then(data => {

        // See the response in the console
        console.log("Booking id is: ");
        console.log(booking_id);
        console.log("Booking data is: ");
        console.log(data);
        console.log("Booking verification status: ");
        console.log(data.is_verified);

        // create the auth string
        // this is the string that will be encoded in the QR code
        const auth_string = data.room + "_Seat" + data.seat;
        console.log("Booking auth string is: ");
        console.log(auth_string);

        // the HTML upload form
        document.getElementById("cameraFileInput")
            .addEventListener("change", e => {
                // when a change event is triggered, i.e. an image is selected

                // create a new FormData object
                const formdata = new FormData()

                // append the image to the FormData object
                formdata.append("image", e.target.files[0])

                // send the FormData object (the image) to the Imgur API
                console.log("UPLOADING IMAGE TO IMGUR")
                fetch("https://api.imgur.com/3/image/", {
                    method: "post",
                    headers: {
                        Authorization: "Client-ID 29513b1e608db48"
                    },
                    body: formdata
                }).then(data => data.json()).then(data => {
                    // store the link to the image returned by the Imgur API
                    const tempURL = data.data.link;
                    console.log("Unencoded URL is " + tempURL);

                    // encode the URL for passing to the GoQR API
                    const encodedURL = encodeURIComponent(tempURL);
                    console.log("Encoded URL is " + encodedURL);

                    // create the complete URL for the GoQR API
                    const completeURL = "http://api.qrserver.com/v1/read-qr-code/?fileurl=" + encodedURL;
                    console.log("Complete URL is " + completeURL);
                    console.log("SENDING IMAGE TO GOQR API FOR PROCESSING")

                    // send the image to the GoQR API for processing
                    fetch(completeURL, {
                        method: "GET"
                    })
                        .then(response => response.json())
                        .then(data => {
                            // if the QR code is successfully read, a JSON object will be returned

                            // the JSON object will contain an array of objects
                            // the first object in the array will contain the data
                            console.log(data[0].symbol[0].data);
                            const qr_data = data[0].symbol[0].data;
                            console.log("QR CODE HAS BEEN PROCESSED");
                            console.log("QR CODE DATA IS: " + qr_data);
                            // check if the booking ID in the QR code matches the booking ID of the booking
                            if (qr_data == auth_string) {
                                // if the booking ID matches, the booking is verified
                                // display a message to the user
                                alert("Your booking has been successfully verified! Thank you for using bookDCU!");

                                // change the booking's is_verified attribute to true
                                window.location.href = "/verify_booking/" + booking_id;

                            } else {
                                // if the booking ID does not match, the booking is not verified
                                // display a message to the user
                                alert("Your booking could not be verified.\n\nPlease ensure you are in the correct room and seat and try again.");
                            }
                        })
                        .catch(error => {
                            // if the QR code is not successfully read, an error will be thrown
                            // display a message to the user
                            alert("Error reading QR code" + error);
                        });
                });
            });
    });
});
