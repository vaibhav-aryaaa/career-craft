// Wait for the entire HTML page to load before running the script
document.addEventListener('DOMContentLoaded', () => {

    // Get references to our HTML elements
    const resumeForm = document.getElementById('resume-form');
    const resumeFile = document.getElementById('resume-file');
    const loader = document.getElementById('loader');
    const resultsDiv = document.getElementById('results');

    // Listen for when the form is submitted
    resumeForm.addEventListener('submit', (event) => {
        // Prevent the default browser action of reloading the page
        event.preventDefault();

        // Show the loader and clear any previous results
        loader.style.display = 'block';
        resultsDiv.innerHTML = '';

        // Create a FormData object to send the file
        const formData = new FormData();
        formData.append('resume', resumeFile.files[0]);

        // Use the Fetch API to send the file to our backend
        fetch('/analyze', {
            method: 'POST',
            body: formData,
        })
        .then(response => {
            // Check if the server responded with an error
            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }
            return response.json(); // Parse the JSON response from the server
        })
        .then(data => {
            // Check if our API sent back an error message
            if (data.error) {
                throw new Error(data.error);
            }
            
            // Format the AI's response into nice HTML
            const careerSuggestionsHTML = data.career_suggestions.map(job => `<li>${job}</li>`).join('');
            
            const resultsHTML = `
                <h2>Career Suggestions</h2>
                <ul>${careerSuggestionsHTML}</ul>
                <h2>Skill Analysis</h2>
                <p>${data.skill_analysis}</p>
            `;
            
            // Display the formatted results
            resultsDiv.innerHTML = resultsHTML;
        })
        .catch(error => {
            // Display any errors that occurred during the process
            resultsDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
        })
        .finally(() => {
            // Hide the loader, whether it succeeded or failed
            loader.style.display = 'none';
        });
    });
});