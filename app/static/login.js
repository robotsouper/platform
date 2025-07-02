document.getElementById("loginForm").addEventListener("submit", function(e) {
  e.preventDefault();
  const name = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  fetch("/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, password })
  })
  .then(res => res.json())
  .then(data => {
    if (data.access_token) {
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("userName", data.name);
      localStorage.setItem("userId", data.user_id);
      window.location.href = "/"; 
    } else {
      alert("Invalid login");
    }
  });
});
