document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('newsletter-form');
  if (!form) return;

  form.addEventListener('submit', async function (e) {
    e.preventDefault();

    const emailInput = document.getElementById('newsletter-email');
    const submitButton = form.querySelector('.newsletter-button');
    const messageDiv = document.getElementById('newsletter-message');

    // Clear previous messages
    messageDiv.className = 'newsletter-message';
    messageDiv.textContent = '';

    // Disable the form
    submitButton.disabled = true;
    submitButton.textContent = 'Subscribing...';

    // Get current page information
    const pageTitle = document.title || 'Unknown Page';
    const pageUrl = window.location.href;
    const pagePath = window.location.pathname;

    // Prepare the data with enhanced context
    const formData = {
      name: 'Newsletter Subscriber', // Default name for newsletter signups
      email: emailInput.value,
      message: `Newsletter signup from: ${pageTitle} | URL: ${pageUrl}`
    };

    try {
      // Send the data to your Cloud Function
      const response = await fetch('https://europe-west1-nlp-api-test-260216.cloudfunctions.net/website-form-to-bq', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });

      const result = await response.json();

      if (response.ok && result.status === 'success') {
        // Success
        messageDiv.className = 'newsletter-message success';
        messageDiv.textContent = 'Success! Welcome to my newsletter. Check your email for confirmation.';

        // Clear the form
        emailInput.value = '';

        // Optional: Track with walkerOS if available
        if (window.elb) {
          window.elb('newsletter_signup', {
            email: formData.email,
            page_title: pageTitle,
            page_url: pageUrl,
            page_path: pagePath
          });
        }
      } else {
        // Error from server
        throw new Error(result.error || 'Subscription failed');
      }
    } catch (error) {
      // Network or other error
      console.error('Newsletter signup error:', error);
      messageDiv.className = 'newsletter-message error';
      messageDiv.textContent = 'Oops! Something went wrong. Please try again later or contact support.';
    } finally {
      // Re-enable the form
      submitButton.disabled = false;
      submitButton.textContent = 'Subscribe';
    }
  });
});