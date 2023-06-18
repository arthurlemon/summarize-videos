let params = new URLSearchParams(window.location.search);
let video_id = params.get('video_id');
let progressBar = document.getElementById('progress-bar');

// Fetch the summary from the backend
fetch(`http://localhost:8000/api/summary/${encodeURIComponent(video_id)}`)
    .then(response => response.json())
    .then(data => {
        console.log(data);  // log the data
        // Display the overall summary
        document.getElementById('overall-summary').textContent = data.summary_all;

        // Display each section summary
        let sectionSummaries = document.getElementById('section-summaries');
        data.summary_sections.forEach(section => {
            // Create a new div for this section
            let div = document.createElement('div');
            div.innerHTML = `
                <h2>${section.start} - ${section.end}</h2>
                <p>${section.summary}</p>
            `;
            // Append the new div to the container
            sectionSummaries.appendChild(div);
        });

        // Remove the progress bar once the data has loaded
        progressBar.style.width = '100%';
        setTimeout(() => progressBar.style.width = '0%', 500);
    });

// Simulate progress updates
let progress = 0;
let progressInterval = setInterval(() => {
    progress += Math.random() * 10;
    if (progress > 100) {
        progress = 100;
        clearInterval(progressInterval);
    }
    progressBar.style.width = progress + '%';
}, 100);
