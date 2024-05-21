//Function which allow user to toggle between text and password on register.html
function togglePassword() {
  var x = document.getElementById("pwd");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}


//Function which makes the input field for updating the email-address on the profile page available and changes the name and type of the button when clicked.
//Keeps track of the buttons state
var isEmailFieldEnabled = false;
function undisable_emailfield() {
  var emailField = document.getElementById("email_field");
  var btnToggle = document.getElementById("btn_toggle");

  if (!isEmailFieldEnabled) {
    emailField.removeAttribute("disabled");
    btnToggle.value = "Spara";
    isEmailFieldEnabled = true;
  } else {
    btnToggle.type = "submit";
  }
}
