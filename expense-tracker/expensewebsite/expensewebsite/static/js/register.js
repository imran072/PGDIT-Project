const usernameField=document.querySelector("#usernameField");
const usernameFeedback=document.querySelector("#username-feedback");
const emailField=document.querySelector("#emailField");
const emailFeedback=document.querySelector("#email-feedback");
const passwordField = document.querySelector("#passwordField");
const togglePassword=document.querySelector(".togglePassword");

const handleToggle = (e) => {
    if (togglePassword.textContent === "SHOW") {
        passwordField.setAttribute("type","text");
        togglePassword.textContent = "HIDE";
    } else {
        togglePassword.textContent = "SHOW";
        passwordField.setAttribute("type","password");
    }
}

togglePassword.addEventListener("click", handleToggle);

usernameField.addEventListener("keyup", (e) => {
    const usernameVal = e.target.value;  
    usernameField.classList.remove("is-invalid");
    usernameFeedback.style.display='none';
    if (usernameVal.length > 0) {
      fetch("/authentication/validate-username", {
        body: JSON.stringify({ username: usernameVal }),
        method: "POST",
      })
        .then((res) => res.json())
        .then((data) => {
            /* console.log('data',data) */
          if (data.username_error) {
            usernameField.classList.add("is-invalid");
            usernameFeedback.style.display='block';
            usernameFeedback.innerHTML=`<p>${data.username_error}</p>`;
          }
        });
    }
  });

  emailField.addEventListener("keyup", (e) => {
    const emailVal = e.target.value;  
    emailField.classList.remove("is-invalid");
    emailFeedback.style.display='none';
    if (emailVal.length > 0) {
      fetch("/authentication/validate-email", {
        body: JSON.stringify({ email: emailVal }),
        method: "POST",
      })
        .then((res) => res.json())
        .then((data) => {
            /* console.log('data',data) */
          if (data.email_error) {
            emailField.classList.add("is-invalid");
            emailFeedback.style.display='block';
            emailFeedback.innerHTML=`<p>${data.email_error}</p>`;
          }
        });
    }
  });