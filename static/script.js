//Function which allow user to toggle between text and password on register.html
function togglePassword() {
  var x = document.getElementById("pwd");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}

//Confirm or disconfirm a published the published post
function runPythonScript() {
      // Get the path to the Python script.
      var pythonScriptPath = "add_vote.py";
      // Run the Python script.
      subprocess.run(["python", pythonScriptPath]);
    }