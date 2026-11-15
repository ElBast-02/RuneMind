
const registerForm = document.getElementById("register-form");
const message = document.getElementById("message");

registerForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    message.textContent = "Creating account...";

    try {
        const response = await fetch("/api/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {
            message.textContent = "Account created successfully! Redirecting to login...";

            window.location.href = "/login";
        } else {
            message.textContent = data.error || "Registration failed.";
        }

    } catch (error) {
        message.textContent = "Unable to connect to the server.";
        console.error("Registration error:", error);
    }
});
