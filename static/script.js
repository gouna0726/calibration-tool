document.getElementById("uploadForm").addEventListener("submit", function(event) {
    event.preventDefault();
    let fileInput = document.getElementById("excelFile").files[0];
    if (!fileInput) {
        alert("Please select an Excel file.");
        return;
    }

    let formData = new FormData();
    formData.append("file", fileInput);

    fetch('/upload_excel', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById("uploadStatus").innerHTML = `<p style="color:red;">Error: ${data.error}</p>`;
        } else {
            document.getElementById("uploadStatus").innerHTML = `<p style="color:green;">File uploaded successfully!</p>`;
            document.getElementById("regressionResults").innerHTML = `
                <strong>Slope:</strong> ${data.slope.toFixed(4)}<br>
                <strong>Intercept:</strong> ${data.intercept.toFixed(4)}<br>
                <strong>R²:</strong> ${data.r_squared.toFixed(4)}
            `;

            // Display the plot
            let imgElement = document.getElementById("calibrationPlot");
            imgElement.src = "data:image/png;base64," + data.plot_url;
            imgElement.style.display = "block";

            // Display Sample Data
            let sampleTable = document.getElementById("sampleTable");
            sampleTable.style.display = "table";
            sampleTable.innerHTML = `<tr>
                <th>Sample Name</th>
                <th>Sample Intensity</th>
                <th>Sample Internal Control</th>
                <th>Normalized Intensity</th>
                <th>Concentration (ppb)</th>
            </tr>`;

            data.sample_data.forEach(sample => {
                let row = sampleTable.insertRow();
                row.insertCell(0).innerText = sample["Sample Name"];
                row.insertCell(1).innerText = sample["Sample Intensity"];
                row.insertCell(2).innerText = sample["Sample Internal Control"];
                row.insertCell(3).innerText = sample["Normalized Intensity"].toFixed(4);
                row.insertCell(4).innerText = sample["Sample Concentration (ppb)"].toFixed(4);
            });
        }
    })
    .catch(error => console.error('Error:', error));
});

