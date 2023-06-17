document.getElementById('summarize-form').addEventListener('submit', function (e) {
    e.preventDefault();
    let url = document.getElementById('video-url').value;
    fetch('http://localhost:8000/api/summarize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: url })
    }).then(response => response.json())
        .then(data => {
            // redirect to summary page
            window.location.href = `summary.html?video_id=${data.video_id}`;
        });
});
