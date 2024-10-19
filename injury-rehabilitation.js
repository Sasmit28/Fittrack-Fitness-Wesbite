let injuriesData = []; // Store reported injuries

// Function to open the injury report form
function openInjuryForm() {
    document.getElementById("injury-form-container").style.display = "block";
}

// Injury report form submission handler
document.getElementById('injury-report-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const injuryName = document.getElementById('injury-name').value;
    const injuryDescription = document.getElementById('injury-description').value;

    // Store the injury data in the injuries array
    injuriesData.push({
        name: injuryName,
        description: injuryDescription
    });

    // Clear the form after submission
    document.getElementById('injury-name').value = '';
    document.getElementById('injury-description').value = '';

    alert('Injury Report Submitted!');
    document.getElementById("injury-form-container").style.display = "none";
});

// Function to suggest a treatment plan based on the reported injury
function treatInjury() {
    const lastInjury = injuriesData[injuriesData.length - 1]; // Get the last reported injury

    if (!lastInjury) {
        alert("No injury reported! Please report an injury first.");
        return;
    }

    let planDetails = '';

    // Basic rehabilitation plans based on injury types
    if (lastInjury.name.toLowerCase().includes("knee")) {
        planDetails = `
            <h3>Knee Injury Treatment Plan</h3>
            <ul>
                <li>Rest the knee and avoid overexertion.</li>
                <li>Apply ice to reduce swelling.</li>
                <li>Physical therapy focused on strengthening exercises.</li>
                <li>Take anti-inflammatory medications as prescribed.</li>
            </ul>
        `;
    } else if (lastInjury.name.toLowerCase().includes("back")) {
        planDetails = `
            <h3>Back Injury Treatment Plan</h3>
            <ul>
                <li>Stretching exercises to improve flexibility.</li>
                <li>Rest and avoid heavy lifting.</li>
                <li>Consider seeing a chiropractor or physical therapist.</li>
                <li>Pain management with over-the-counter medications.</li>
            </ul>
        `;
    } else if (lastInjury.name.toLowerCase().includes("shoulder")) {
        planDetails = `
            <h3>Shoulder Injury Treatment Plan</h3>
            <ul>
                <li>Use a cold compress to reduce swelling.</li>
                <li>Perform shoulder strengthening exercises under guidance.</li>
                <li>Avoid activities that put pressure on the shoulder.</li>
            </ul>
        `;
    } else {
        // Default rehabilitation plan for general injuries
        planDetails = `
            <h3>General Injury Treatment Plan</h3>
            <ul>
                <li>Rest the affected area.</li>
                <li>Apply ice to reduce swelling.</li>
                <li>Consider physical therapy to regain strength and flexibility.</li>
                <li>Follow medical advice and take medications as prescribed.</li>
            </ul>
        `;
    }

    // Display the treatment plan
    document.getElementById("rehab-plan").style.display = "block";
    document.getElementById("plan-details").innerHTML = planDetails;
}

// Assuming you have a field or mechanism for determining the injury grade
const injuryGrade = document.querySelector('input[name="injury-grade"]:checked').value; // Retrieve selected injury grade

// Save to localStorage
localStorage.setItem('injuryGrade', injuryGrade);
