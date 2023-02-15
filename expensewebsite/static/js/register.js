const usernameField = document.querySelector('#usernameField');
const feedbackArea = document.querySelector(".invalid-feedback");
const emailField = document.querySelector('#emailField');
const emailFeedbackArea = document.querySelector(".invalid-email-feedback");
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");
const emailSuccessOutput = document.querySelector(".emailSuccessOutput");

usernameField.addEventListener('keyup', (e) => {
    const usernameVal = e.target.value;
    usernameSuccessOutput.style.display='block';
    usernameSuccessOutput.textContent=`Checking ${usernameVal}`

    usernameField.classList.remove("is-invalid");
    feedbackArea.style.display='none';

    if(usernameVal.length > 0) {
        fetch('/authentication/validate-username', {
            body: JSON.stringify({username: usernameVal}),
            method: "POST",
        }).then(res => res.json())
        .then(data => {
            usernameSuccessOutput.style.display='none';
            if(data.username_error) {
                usernameField.classList.add("is-invalid");
                feedbackArea.style.display='block';
                feedbackArea.innerHTML= `<p>${data.username_error}</p>`;
            }
        })
    }

})

emailField.addEventListener('keyup', (e) => {
    const emailVal = e.target.value;
    emailSuccessOutput.style.display='block';
    emailSuccessOutput.textContent=`Checking ${emailVal}`

    emailField.classList.remove("is-invalid");
    emailFeedbackArea.style.display='none';

    if(emailVal.length > 0) {
        fetch('/authentication/validate-email', {
            body: JSON.stringify({email: emailVal}),
            method: "POST",
        }).then(res => res.json())
        .then(data => {
            emailSuccessOutput.style.display='none';
            if(data.email_error) {
                emailField.classList.add("is-invalid");
                emailFeedbackArea.style.display='block';
                emailFeedbackArea.innerHTML= `<p>${data.email_error}</p>`;
            }
        })
    }

})