document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registrationForm') || document.getElementById('loginForm');
    if (form) form.addEventListener('submit', handleFormSubmit);
  
    if (document.getElementById('password')) {
      document.getElementById('password').addEventListener('input', checkPasswordStrength);
    }
  
    if (document.getElementById('captchaCanvas')) {
      generateCaptcha();
    }
  });
  
  function handleFormSubmit(event) {
    event.preventDefault();
    const password = document.getElementById('password').value
    const username = document.getElementById('username').value
    const email = document.getElementById('Email').value
    const fullname = document.getElementById('Fullname').value
    const address = document.getElementById('Address').value
    const phone = document.getElementById('phone').value
    const passwordConfirmation = document.getElementById("confirmPassword").value

    const data = {
      password, username, email, fullname, address, phone_number : phone
    }

    
    if (validateCaptcha()) {
      console.log("registering ")
      if (password !== passwordConfirmation) {
        return alert("Passwords Doesnt Match!!!")
      }
      async function Register() {
        try {
          const options = {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json' // Indicates that the data is in JSON format
            },
            body: JSON.stringify(data) 
          }
          const response = await fetch("http://127.0.0.1:5000/user", options)
          if (response.ok) {
            const result = await response.json();  // Parse JSON from response
            console.log(result);  // Output: "User rakesh added successfully!"
          } else {
            console.error('Failed to add user:', response.status);
          }
        } catch (error) {
          console.error(error)
        }
      }
      Register()
      // alert('Registration successful! Your encrypted password is: ' + encryptedPassword);
      // window.location.href = "login.html";  // Redirect to login page after successful registration
    } else {
      alert('Captcha validation failed!');
    }
  }

  async function loginHandler() {
    try {

      const password = document.getElementById('loginPassword').value
      const username = document.getElementById('username').value

      const data = {username, password}

      const options = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json' // Indicates that the data is in JSON format
        },
        body: JSON.stringify(data) 
      }
      const response = await fetch("http://127.0.0.1:5000/login", options)
      if (response.ok) {
        const result = await response.json();  // Parse JSON from response
        console.log(result);  // Output: "User rakesh added successfully!"
      } else {
        console.error('Failed to add user:', response.status);
      }
    } catch (error) {
      console.error(error)
      alert(error.message)
    }
  }
  
  function checkPasswordStrength() {
    const password = document.getElementById('password').value;
    const feedback = document.getElementById('passwordFeedback');
    const strength = getPasswordStrength(password);
    feedback.innerText = `Password strength: ${strength}`;
    if (strength === "Weak" || strength === "Very Weak") {
      feedback.setAttribute("style", "color: red")
    } else if (strength === "Medium") {
      feedback.setAttribute("style", "color: #d1a804")

    } else if (strength === "Strong" || strength === "Very Strong") {
      feedback.setAttribute("style", "color: green")

    } 
  }
  
  function getPasswordStrength(password) {
    let strength = 0;
    if (password.length >= 8) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^A-Za-z0-9]/.test(password)) strength++;
    
    switch (strength) {
      case 5: return 'Very Strong';
      case 4: return 'Strong';
      case 3: return 'Medium';
      case 2: return 'Weak';
      default: return 'Very Weak';
    }
  }
  
  let captchaText = '';
  
  function generateCaptcha() {
    const canvas = document.getElementById('captchaCanvas');
    const context = canvas.getContext('2d');
    canvas.width = 200;
    canvas.height = 50;
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.font = '30px Arial';
    captchaText = Math.random().toString(36).substring(2, 8);
    context.fillText(captchaText, 50, 35);
  }
  
  function validateCaptcha() {
    const captchaInput = document.getElementById('captchaInput').value;
    return captchaInput === captchaText;
  }
  
  function logout() {
    alert("You have been logged out.");
    window.location.href = "login.html";  // Redirect to login page after logout
  }

  const loginFrom = document.querySelector("#loginForm")

  loginFrom.addEventListener("submit", loginHandler)
  