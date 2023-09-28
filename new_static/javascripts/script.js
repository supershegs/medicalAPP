document.getElementById('registration-form').addEventListener('submit', function(event) {
    var password = document.getElementById('password').value;
    var passwordConfirmation = document.getElementById('password-confirmation').value;

    if (password !== passwordConfirmation) {
        alert('Passwords do not match. Please try again.');
        event.preventDefault(); // Prevent the form from submitting
    }
});

document.getElementById('imageInput').addEventListener('change', function(event) {
    var imageFile = event.target.files[0];
    var imageElement = document.getElementById('displayImage');

    if (imageFile) {
        var imageUrl = URL.createObjectURL(imageFile);
        imageElement.src = imageUrl;
        imageElement.style.display = 'block';
    }
});

// Function to capture a photo from the device camera
// document.getElementById('cameraButton').addEventListener('click', function() {
//     var imageElement = document.getElementById('displayImage');

//     // Check if the browser supports the getUserMedia API
//     if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
//         navigator.mediaDevices.getUserMedia({ video: true })
//         .then(function(stream) {
//             var videoElement = document.createElement('video');
//             document.body.appendChild(videoElement);
//             videoElement.srcObject = stream;
//             videoElement.play();

//             // Capture a frame from the video stream
//             setTimeout(function() {
//                 var canvas = document.createElement('canvas');
//                 canvas.width = videoElement.videoWidth;
//                 canvas.height = videoElement.videoHeight;
//                 var context = canvas.getContext('2d');
//                 context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
//                 var imageUrl = canvas.toDataURL('image/jpeg');

//                 // Display the captured photo
//                 imageElement.src = imageUrl;
//                 imageElement.style.display = 'block';

//                 // Stop the video stream and remove the video element
//                 stream.getTracks().forEach(function(track) {
//                     track.stop();
//                 });
//                 videoElement.remove();
//             }, 1000); // Adjust the delay as needed
//         })
//         .catch(function(error) {
//             console.error('Error accessing camera:', error);
//         });
//     } else {
//         alert('Your browser does not support camera access.');
//     }
// });