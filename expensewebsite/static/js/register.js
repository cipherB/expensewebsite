const usernameField = document.querySelector('#usernameField');
const feedbackArea = document.querySelector(".invalid-feedback");
const emailField = document.querySelector('#emailField');
const emailFeedbackArea = document.querySelector(".invalid-email-feedback");
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");
const emailSuccessOutput = document.querySelector(".emailSuccessOutput");
const passwordField = document.querySelector('#passwordField');
const showPasswordToggle = document.querySelector('.showPasswordToggle');
const submitBtn = document.querySelector('.submit-btn');

usernameField.addEventListener('keyup', (e) => {
    // Validate username if it exists contains valid characters and above 0
    const usernameVal = e.target.value;
    usernameSuccessOutput.style.display='block';
    usernameSuccessOutput.textContent=`Checking ${usernameVal}`

    usernameField.classList.remove("is-invalid");
    feedbackArea.style.display='none';
    submitBtn.disabled = true;

    if(usernameVal.length > 0) {
        fetch('/authentication/validate-username', {
            body: JSON.stringify({username: usernameVal}),
            method: "POST",
        }).then(res => res.json())
        .then(data => {
            usernameSuccessOutput.style.display='none';
            if(data.username_error) {
                // disable submit button and show error message if invalid
                submitBtn.disabled = true;
                usernameField.classList.add("is-invalid");
                feedbackArea.style.display='block';
                feedbackArea.innerHTML= `<p>${data.username_error}</p>`;
            } else {
                submitBtn.removeAttribute('disabled');
            }
        })
    }

})

emailField.addEventListener('keyup', (e) => {
    // Validate user email if it exists, or is a valid email format
    const emailVal = e.target.value;
    emailSuccessOutput.style.display='block';
    emailSuccessOutput.textContent=`Checking ${emailVal}`

    emailField.classList.remove("is-invalid");
    emailFeedbackArea.style.display='none';
    submitBtn.disabled = true;

    if(emailVal.length > 0) {
        fetch('/authentication/validate-email', {
            body: JSON.stringify({email: emailVal}),
            method: "POST",
        }).then(res => res.json())
        .then(data => {
            emailSuccessOutput.style.display='none';
            if(data.email_error) {
                // if email is invalid, disable submit button and display error message
                // submitBtn.setAttribute('disabled','disabled');
                submitBtn.disabled = true;
                emailField.classList.add("is-invalid");
                emailFeedbackArea.style.display='block';
                emailFeedbackArea.innerHTML= `<p>${data.email_error}</p>`;
            } else {
                submitBtn.removeAttribute('disabled');
            }
        })
    }

})

const handletoggleInput = (e) => {
    // Toggle password visibility
    //
    if(showPasswordToggle.textContent==='SHOW') {
        showPasswordToggle.textContent='HIDE';

        passwordField.setAttribute('type', 'text');
    } else {
        showPasswordToggle.textContent='SHOW';

        passwordField.setAttribute('type', 'password');
    }
}

showPasswordToggle.addEventListener('click',handletoggleInput);