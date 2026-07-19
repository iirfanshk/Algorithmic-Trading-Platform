document.addEventListener("DOMContentLoaded", () => {

    const signupBtn = document.getElementById("signupBtn");

    signupBtn.addEventListener("click", async () => {

        const username = document.getElementById("username").value.trim();
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;
        const confirm = document.getElementById("confirm").value;

        if (!username || !email || !password || !confirm) {
            alert("Please fill all fields.");
            return;
        }

        if (password !== confirm) {
            alert("Passwords do not match.");
            return;
        }

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

            if (data.success) {

                alert("Account created successfully!");

                window.location.href = "/";

            } else {

                alert(data.message);

            }

        } catch (error) {

            console.error(error);

            alert("Unable to connect to server.");

        }

    });

});