console.log("Settings JS Loaded");
document.addEventListener("DOMContentLoaded", () => {

    const saveBtn = document.getElementById("saveSettingsBtn");
    saveBtn.addEventListener("click", async () => {

    console.log("Save button clicked");


        const payload = {

            theme: document.getElementById("theme").value,

            capital: document.getElementById("defaultCapital").value,

            commission: document.getElementById("commission").value,

            slippage: document.getElementById("slippage").value,

            stoploss: document.getElementById("stoploss").value,

            takeprofit: document.getElementById("takeprofit").value

        };

        try{

            const response = await fetch("/api/settings",{

                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify(payload)

            });

            const result = await response.json();

            alert(result.message);

        }

        catch(err){

            console.error(err);

            alert("Unable to save settings.");

        }

    });

});