//Function which allow user to toggle between text and password on register.html
function togglePassword() {
  var x = document.getElementById("pwd");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}

document.querySelector('form').addEventListener('submit', function (e) {
  var pwd = document.getElementById("pwd").value;
  var confirm_pwd = document.getElementById("confirm_pwd").value;
  if (pwd !== confirm_pwd) {
    e.preventDefault();
    alert("Lösenorden matchar inte.");
  }
});

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


//Function which is used on the profile page to open a modal
function openDeleteModal() {
                    var modal = document.getElementById("deleteModal");
                    modal.style.display = "block";
                }

                function closeDeleteModal() {
                    var modal = document.getElementById("deleteModal");
                    modal.style.display = "none";
                }


//Function which is used on the profile page to open a modal
function openLogoutModal() {
  var modal = document.getElementById("logouteModal");
  modal.style.display = "block";
}

function closeLogoutModal() {
  var modal = document.getElementById("logouteModal");
  modal.style.display = "none";
}
