document.getElementById("contact-form").addEventListener("submit", async function (event) {
    event.preventDefault();  // Prevent default form submission

    // Gather form data
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const message = document.getElementById("message").value;

    // Create the form data object to be sent
    const formData = {
        name: name,
        email: email,
        message: message
    };

    try {
        // cloud function endpoint
        const customEndpoint = "https://europe-west1-nlp-api-test-260216.cloudfunctions.net/website-form-to-bq"
        // Send the POST request using fetch
        const response = await fetch(customEndpoint, {
            method: "POST", // Use the POST method
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(formData),
        });

        // Check if the request was successful (status code 200-299)
        if (response.ok) {
            // Show the success message
            document.getElementById("form-success-message").style.display = "block";
            document.getElementById("form-error-message").style.display = "none";

            // Optionally clear the form fields
            document.getElementById("contact-form").reset();
        } else {
            // Show error message if the response status is not ok
            document.getElementById("form-error-message").style.display = "block";
            document.getElementById("form-success-message").style.display = "none";
        }
    } catch (error) {
        // Show error message in case of any network or other errors
        document.getElementById("form-error-message").style.display = "block";
        document.getElementById("form-success-message").style.display = "none";
        console.error("Error submitting the form:", error);
    }
});