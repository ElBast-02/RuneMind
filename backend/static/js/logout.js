
const logoutButton = document.getElementById("logout-button");
const logoutMessage = document.getElementById("logout-message");

logoutButton.addEventListener("click", async function () {
    logoutButton.disabled = true;
    logoutMessage.textContent = "Logging out...";

    try {
        const response = await fetch("/api/logout", {
            method: "POST",
            credentials: "same-origin"
        });

        if (response.ok) {
            window.location.href = "/login";
        } else {
            logoutMessage.textContent = "Logout failed. Please try again.";
            logoutButton.disabled = false;
        }

    } catch (error) {
        logoutMessage.textContent = "Unable to connect to the server.";
        logoutButton.disabled = false;
        console.error("Logout error:", error);
    }
});
