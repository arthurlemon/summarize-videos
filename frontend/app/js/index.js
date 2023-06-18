document.getElementById('summarize-form').addEventListener('submit', function (e) {
    e.preventDefault();
    let url = document.getElementById('video-url').value;
    // Extract video id
    let video_id = url.split("v=")[1];
    // redirect to summary page
    window.location.href = `summary.html?video_id=${video_id}`;

    // Then start fetch operation
    fetch('http://localhost:8000/api/summarize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: url })
    }).then(response => response.json())
        .then(data => {
            console.log(data);
        });
});
