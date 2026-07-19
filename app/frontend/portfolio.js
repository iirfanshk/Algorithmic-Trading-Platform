document.addEventListener("DOMContentLoaded", () => {

    const tradeBtn = document.getElementById("executeTradeBtn");

    const asset = document.getElementById("asset");

    const quantity = document.getElementById("quantity");

    const tradeType = document.getElementById("trade_type");

    tradeBtn.addEventListener("click", async () => {

        if (quantity.value.trim() === "" || Number(quantity.value) <= 0) {

            alert("Please enter a valid quantity.");

            return;

        }

        tradeBtn.disabled = true;
        tradeBtn.innerText = "Executing...";

        try {

            const response = await fetch("/api/trade", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    asset: asset.value,

                    trade_type: tradeType.value,

                    quantity: Number(quantity.value)

                })

            });

            const result = await response.json();

            if (response.ok && result.success) {

                alert("✅ Trade Executed Successfully");

                location.reload();

            } else {

                alert(result.message || "Trade Failed");

            }

        }

        catch (err) {

            console.error(err);

            alert("Unable to connect to server.");

        }

        finally {

            tradeBtn.disabled = false;

            tradeBtn.innerText = "Execute Trade";

        }

    });

});