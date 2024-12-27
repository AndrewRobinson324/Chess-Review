document.getElementById('pgnForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const fileInput = document.getElementById('pgnFile');  // Corrected to define fileInput
    const file = fileInput.files[0];

    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const pgn = e.target.result;
            fetch('/games', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ pgn: pgn })
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                alert(data.message);  // Add an alert to show the response message
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while analyzing the game.');
            });
        };
        reader.readAsText(file);
    } else {
        alert("Please select a PGN file to upload.");
    }
});