const usernameFeedback = document.querySelector(".username_feedback");
const emailFeedback = document.querySelector(".email_feedback");
const nameFeedback = document.querySelector(".name_feedback");
const confirmPasswordFeedback = document.querySelector(".confirmPassword_feedback");

nameField = document.querySelector("#name");
usernameField =  document.querySelector("#username");
emailField =  document.querySelector("#email");
passwordField =  document.querySelector("#password1");
confirmPasswordField = document.querySelector("#password2");
submitButton =  document.querySelector("#submit_button");


nameField.addEventListener("keyup", (e) => {
    const nameVal = e.target.value; 
    nameFeedback.style.display = "none"; 
    nameFeedback.classList.remove("is-invalid");

    fetch('/validate_name', {
        body: JSON.stringify({name: nameVal}), 
        method: "POST", 
    }).then(res => res.json())
    .then(data => {
        if (data.name_error)
        {
            nameFeedback.style.display = "block";
            nameFeedback.innerHTML = `<p>${data.name_error}</p>`;
            nameField.classList.add('is-invalid')
            submitButton.disabled=true;
        }
        else 
            submitButton.removeAttribute('disabled');
    })
});

usernameField.addEventListener("keyup", (e) => {
    const usernameVal = e.target.value; 
    usernameFeedback.style.display = "none"; 
    usernameField.classList.remove('is-invalid');

    fetch('/validate_username', {
        body: JSON.stringify({username: usernameVal}),
        method: "POST", 
    }).then(res => res.json())
    .then(data => {
        if (data.username_error)
        {
            usernameFeedback.style.display = 'block';
            usernameFeedback.innerHTML = `<p>${data.username_error}</p>`;
            usernameField.classList.add('is-invalid')
            submitButton.disabled=true;
        }
        else {
            submitButton.removeAttribute("disabled");
        }
    })

    
});

emailField.addEventListener("keyup", (e) => {
    const emailVal = e.target.value; 

    emailFeedback.style.display = "none"; 
    emailFeedback.classList.remove("is-invalid");

    fetch('/validate_email', {
        body: JSON.stringify({email: emailVal}),
        method: "POST", 
    }).then(res => res.json())
    .then(data => {
        if (data.email_error)
        {
            emailField.classList.add('is-invalid');
            emailFeedback.style.display = "block";
            emailFeedback.innerHTML = `<p>${data.email_error}</p>`;
            submitButton.disabled=true;

        }
        else 
            submitButton.removeAttribute("disabled");
    })
});

confirmPasswordField.addEventListener("keyup", (e) => {
    pass = e.target.value; 
    confirmPasswordFeedback.style.display = "none"; 
    console.log("hhhh", 111)
    confirmPasswordFeedback.classList.remove("is-invalid");
    if (pass != passwordField.value)
    {
        confirmPasswordField.classList.add('is-invalid');
        confirmPasswordFeedback.style.display = "block";
        confirmPasswordFeedback.innerHTML = `<p>Passwords do not match</p>`;
        submitButton.disabled=true;
    }
    else 
        submitButton.removeAttribute("disabled");
});

