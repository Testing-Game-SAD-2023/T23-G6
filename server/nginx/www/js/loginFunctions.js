function RegistraGiocatore(){
    var email = document.getElementById("registerEmail").value;
    var password = String(document.getElementById("registerPassword").value);
    var password2 = String(document.getElementById("registerRepeatPassword").value);
    var name = document.getElementById("registerName").value;
    var surname = document.getElementById("registerSurname").value;
    var degree = document.getElementById("registerDegree").value;
    var check = document.getElementById("registerCheck").checked;

    const validateEmail =  String(email).toLowerCase().match(/\b[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,6}\b/g);
    const validateName = String(name).toLowerCase().match(/^[A-Za-zèùàòé][a-zA-Z'èùàòé ]*$/g);
    const validateSurname = String(surname).toLowerCase().match(/^[A-Za-zèùàòé][a-zA-Z'èùàòé ]*$/g);

    if (check == false){
      alert("Please agree to the terms");
    }
    else if (validateEmail == null){
      alert("Invalid email");
    }
    else if (password.length < 7  || password.length > 32 ){
      alert("Invalid password size");
    }
    else if (password != password2) {
      alert("Passwords do not match");
    }
    else if (validateName == null){
      alert("Invalid Name");
    }
    else if (validateSurname == null){
      alert("Invalid Surname");
    }
    else {
      var user = new Object();
      user.NAME = validateName[0];
      user.SURNAME = validateSurname[0];
      user.EMAIL = validateEmail[0];
      user.DEGREE = degree;
      user.PW = password;
      var jsonString= JSON.stringify(user);

      console.log(jsonString);

      fetch('http://127.0.0.1/api/RegistraGiocatore', {
          method: 'POST',
          body: jsonString
      })
      .then(response => response.json())
      .then(response => console.log(JSON.stringify(response)))
      .then(response => alert("CONFIRMATION EMAIL has been sent to "+user.EMAIL))
      .catch(error => alert("Registration failed! Check your connection"));
    }
}

function LoginGiocatore() {
    var email = document.getElementById("loginEmail").value;
    var password = String(document.getElementById("loginPassword").value);
    var rememberme = document.getElementById("loginCheck").checked;

    const validateEmail =  String(email).toLowerCase().match(/\b[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,6}\b/g);

    if (validateEmail == null){
      alert("Invalid email");
    }
    else {
      var user = new Object();
      user.EMAIL = validateEmail[0];
      user.PW = password;
      var jsonString = JSON.stringify(user);

      console.log(jsonString);

      fetch('http://127.0.0.1/api/LoginGiocatore', {
        method: 'POST',
        withCredentials: true,
        headers: {
          "Access-Control-Allow-Origin": "http://127.0.0.1:1200",
          'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: jsonString
      })
        .then(response => response.json())
        .then(response => location.href = response['REDIRECT'])
        .then(response => console.log(response))
      .catch(error => alert("Invalid credentials! Check the email and the password you've typed"));
    }

}

function redirect(){
  let requestBody = new Object();
  requestBody.LOC = location.pathname.split("/").slice(-1).toString()

  let jsonString = JSON.stringify(requestBody);

  fetch('http://127.0.0.1/api/Redirect', {
    method: 'POST',
    withCredentials: true,
    headers: {
      "Access-Control-Allow-Origin": "http://127.0.0.1:1200",
      'Content-Type': 'application/json'
    },
    credentials: 'include',
    body: jsonString
  })
    .then(response => response.json())
    .then(response => {
      if (response['REDIRECT'] == requestBody.LOC)
        document.getElementById("htmlTag").hidden = false;
      else
        location.href = response['REDIRECT']
    })

}

function LogOut(){
  fetch('http://127.0.0.1/api/LogOut', {
    method: 'POST',
    withCredentials: true,
    headers: {
      "Access-Control-Allow-Origin": "http://127.0.0.1:1200",
      'Content-Type': 'application/json'
    },
    credentials: 'include'
  })
    .then(response => response.json())
    .then(response => location.href = response['REDIRECT'])
  .catch(error => console.log(error))
}

function initializePage(){
  redirect()
}

function ConfermaEmail() {
  let code = document.getElementById("secretCode").value
  let requestBody = new Object();
  requestBody.CODE = code

  let jsonString = JSON.stringify(requestBody);

  fetch('http://127.0.0.1/api/ConfermaEmail', {
    method: 'POST',
    withCredentials: true,
    headers: {
      "Access-Control-Allow-Origin": "http://127.0.0.1:1200",
      'Content-Type': 'application/json'
    },
    credentials: 'include',
    body: jsonString
  })
    .then(response => response.json())
    .then(response => {
      if (response['MSG'] == 'Success')
        location.href = response['REDIRECT']
      else
        alert("Wrong code!")
    })
}

function RecuperaAccountInviaEmail()
{
  let requestBody = new Object();
  requestBody.EMAIL = document.getElementById("emailInput").value
  email2 = document.getElementById("emailInput2").value

  if(requestBody.EMAIL !== email2)
    alert("The emails' fields don't match!")
  else{
    let jsonString = JSON.stringify(requestBody);
    fetch('http://127.0.0.1/api/RecuperaAccountInviaEmail', {
      method: 'POST',
      withCredentials: true,
      headers: {
        "Access-Control-Allow-Origin": "http://127.0.0.1:1200",
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: jsonString
    })
      .then(response => response.json())
      .then(response => {
        if (response['MSG'] == 'Success')
        {
          document.getElementById("divEmail1").hidden = true 
          document.getElementById("divEmail2").hidden = true
          document.getElementById("sendEmailText").hidden = true
          document.getElementById("sendEmailButton").hidden = true

          document.getElementById("divpw1").hidden = false 
          document.getElementById("divpw2").hidden = false
          document.getElementById("TypeCodeText").hidden = false
          document.getElementById("divCode").hidden = false
          document.getElementById("ChangePasswordButton").hidden = false
        }
        else
          alert("Failed!")
      })
  }
}

function RecuperaAccountCambiaPassword()
{
  let requestBody = new Object();
  requestBody.CODE = document.getElementById("codeInput").value
  requestBody.PW = document.getElementById("passwordInput1").value

  console.log(requestBody)

  if(requestBody.PW !== document.getElementById("passwordInput2").value)
    alert("The passwords' fields don't match!")
  else{
    let jsonString = JSON.stringify(requestBody);
    fetch('http://127.0.0.1/api/RecuperaAccountCambiaPassword', {
      method: 'POST',
      withCredentials: true,
      headers: {
        "Access-Control-Allow-Origin": "http://127.0.0.1:1200",
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: jsonString
    })
      .then(response => response.json())
      .then(response => {
        if (response['MSG'] == 'Success')
        {
          alert("Password changed!")
        }
        else
          alert("Failed!")
      })
  }
}