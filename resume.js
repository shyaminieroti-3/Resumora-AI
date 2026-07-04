async function analyzeResume() {

    const file = document.getElementById("resumeFile").files[0];

    if (!file) {
        alert("Please select a PDF resume.");
        return;
    }

    const formData = new FormData();
    formData.append("resume", file);

    try {

        const response = await fetch("http://127.0.0.1:5000/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            alert(data.error);
            return;
        }

        // Show success message
        alert(data.message);

        // Extract ATS Score from AI response
        const atsMatch = data.analysis.match(/ATS Score[:\s]*(\d+)/i);

        if (atsMatch) {
            document.getElementById("ats").innerHTML = atsMatch[1] + "%";
        } else {
            document.getElementById("ats").innerHTML = "Completed";
        }

        // Update Status Cards
        document.getElementById("grammar").innerHTML = "Gemini AI";
        document.getElementById("skills").innerHTML = "Resume Analyzed";

        // Display Full AI Report
        document.getElementById("analysisBox").innerHTML =
            `<pre>${data.analysis}</pre>`;

    } catch (error) {

        console.error(error);

        alert("Backend connection failed.\n\nMake sure Flask is running on http://127.0.0.1:5000");

    }

}