let webcamOpen = false;

function openWebcam() {
    const video = document.getElementById('video');
    const snapshotButton = document.querySelector('button[onclick="takeSnapshot()"]');

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
            video.style.display = 'block';
            snapshotButton.style.display = 'block';
            webcamOpen = true;
        })
        .catch(err => console.error("Error accessing webcam: ", err));
}

async function takeSnapshot() {
    if (!webcamOpen) {
        console.error("Webcam not open");
        return;
    }

    const video = document.getElementById('video');
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    const imageData = canvas.toDataURL('image/png');
    sendDataToBackend(imageData);
}

async function sendDataToBackend(imageData) {
    const response = await fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: imageData }),
    });

    const result = await response.json();
    displayResult(result);
}

function displayResult(result) {
    const resultDiv = document.getElementById('result');
    const emojiDiv = document.getElementById('emoji');
    const predictedImageDiv = document.getElementById('predictedImage');

    const emojiFilenames = {
        '#Angry': 'Angry.png',
        '#Disgust': 'Disgust.png',
        '#Fear': 'Fear.png',
        '#Happy': 'Happy.png',
        '#Neutral': 'Neutral.png',
        '#Sad': 'Sad.png',
        '#Surprised': 'Surprised.png',
    };

    const emojiFilename = emojiFilenames[result.predicted_label];

    emojiDiv.innerHTML = `<img src="/static/emojis/${emojiFilename}" alt="${result.predicted_label}" style="height: 230px;">`;

    resultDiv.textContent = `Predicted Emotion: ${result.predicted_label}`;

    predictedImageDiv.innerHTML = `<img src="data:image/jpeg;base64,${result.predicted_image}" alt="Predicted Image" style="max-width: 100%;">`;

    recommendSong(result.predicted_label);
}

async function recommendSong(emotion) {
    const recommendedSongDiv = document.getElementById('recommendedSong');
    let recommendedSongs = [];

    const csvFile = `/static/songs/${emotion.toLowerCase().substring(1)}.csv`;
    const response = await fetch(csvFile);
    const csvData = await response.text();

    Papa.parse(csvData, {
        header: true,
        dynamicTyping: true,
        complete: (result) => {
            recommendedSongs = result.data;
            displayRecommendedSongs();
        },
        error: (err) => {
            console.error("Error parsing CSV:", err);
        }
    });

    function displayRecommendedSongs() {
        recommendedSongs = shuffleArray(recommendedSongs);
    
        const selectedSongs = recommendedSongs.slice(0, 5);
    
        let tableHTML = `<p>Recommended Songs for ${emotion}:</p>
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>Name</th>
                                    <th>Artist</th>
                                    <th>Album</th>
                                </tr>
                            </thead>
                            <tbody>`;
    
        tableHTML += selectedSongs.map(song => `
                        <tr>
                            <td><a href="${song.Spotify_Link}" target="_blank">${song.Name}</a></td>
                            <td>${song.Artist}</td>
                            <td>${song.Album}</td>
                        </tr>`).join('');
    
        tableHTML += `</tbody>
                    </table>`;
    
        recommendedSongDiv.innerHTML = tableHTML;
    }
    

    function shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
    }
}
