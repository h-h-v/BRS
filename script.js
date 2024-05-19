// Get the modal and the login button
var modal = document.getElementById("loginModal");
var loginBtn = document.getElementById("loginBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the login button, open the modal
loginBtn.onclick = function() {
  modal.style.display = "block";
  modal.classList.add("floatIn");
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
  modal.classList.remove("floatIn");
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
    modal.classList.remove("floatIn");
  }
}

// Function to handle successful login
function handleLogin(username) {
  // Create a span element to display the username
  var usernameSpan = document.createElement("span");
  usernameSpan.textContent = username;
  
  // Append the span element to the navigation bar
  var navBar = document.getElementById("navBar");
  navBar.appendChild(usernameSpan);
  
  // Hide the login button
  loginBtn.style.display = "none";
}
