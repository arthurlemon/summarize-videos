let params = new URLSearchParams(window.location.search);
let video_id = params.get('video_id');

window.onload = function() {
    fetchSummary(video_id);
  }

// Fetch the summary from the backend
function fetchSummary(video_id) {
    fetch(`http://localhost:8000/api/summary/${encodeURIComponent(video_id)}`)
        .then(response => response.json())
        .then(data => {
            console.log(data);  // log the data
            // Display the overall summary
            document.getElementById('overall-summary').innerHTML = `
            <a href="https://youtube.com/watch?v=${video_id}">Watch the original video</a>
            <p>${data.summary_all}</p>
            `;

            // Display each section summary
            let sectionSummaries = document.getElementById('section-summaries');
            data.summary_sections.forEach(section => {
                // Create a new div for this section
                let div = document.createElement('div');
                div.innerHTML = `
                    <strong><a href="https://youtube.com/watch?v=${video_id}&t=${Math.round(section.start * 60)}" target="_blank">${formatTime(section.start)} - ${formatTime(section.end)}</a></strong>
                    <p>${section.summary}</p>
                `;
                // Append the new div to the container
                sectionSummaries.appendChild(div);
            });

            // After setting the data, remove the 'hide' class from headers
            document.getElementById('overall-header').classList.remove('hide');
            document.getElementById('section-header').classList.remove('hide');
            // Hide the loader
            document.getElementById('loader').style.display = 'none';
        });
    }
function formatTime(time) {
    let hours = Math.floor(time);
    let minutes = Math.round((time - hours) * 60);
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
}
