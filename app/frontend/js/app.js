document.addEventListener("DOMContentLoaded", () => {

    const loginBtn = document.getElementById("loginBtn");

    if (!loginBtn) return;

    loginBtn.addEventListener("click", async () => {

        const username = document.getElementById("username").value.trim();
        const password = document.getElementById("password").value;

        if (!username || !password) {

            alert("Please enter your username/email and password.");

            return;

        }

        try {

            const response = await fetch("/api/login", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    username: username,
                    password: password

                })

            });

            const data = await response.json();

            if (data.success) {

                // Redirect to Flask dashboard
                window.location.href = "/dashboard";

            } else {

                alert(data.message);

            }

        } catch (error) {

            console.error(error);

            alert("Unable to connect to server.");

        }

    });

});