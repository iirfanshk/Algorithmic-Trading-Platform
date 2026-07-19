document.addEventListener("DOMContentLoaded", () => {

    const ASSETS = {
        Stocks: ["AAPL","MSFT","NVDA","GOOGL","META","AMZN","TSLA"],
        Crypto: ["BTC-USD","ETH-USD","SOL-USD","BNB-USD","XRP-USD"],
        Forex: ["EURUSD=X","GBPUSD=X","USDJPY=X","USDINR=X"],
        Indices: ["^GSPC","^IXIC","^DJI","^NSEI","^NSEBANK"],
        Commodities: ["GC=F","SI=F","CL=F","NG=F"]
    };

    const assetClass = document.getElementById("asset_class");
    const asset = document.getElementById("asset");

    function updateAssets(){

        asset.innerHTML = "";

        ASSETS[assetClass.value].forEach(symbol => {

            const option = document.createElement("option");

            option.value = symbol;
            option.textContent = symbol;

            asset.appendChild(option);

        });

    }

    updateAssets();

    assetClass.addEventListener("change", updateAssets);

    document.getElementById("checkAlertBtn").addEventListener("click", async () => {

        const payload = {

            asset: asset.value,

            condition: document.getElementById("condition").value,

            target_price: document.getElementById("targetPrice").value

        };

        try{

            const response = await fetch("/api/alerts",{

                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify(payload)

            });

            const result = await response.json();

            if(!result.success){

                alert(result.message);

                return;

            }

            const div = document.getElementById("alertResult");

            if(result.triggered){

                div.innerHTML = `
                    <h2 style="color:#22c55e;">
                        🔔 Alert Triggered
                    </h2>

                    <br>

                    <p><b>Asset:</b> ${result.asset}</p>

                    <p><b>Current Price:</b> $${result.current_price}</p>

                    <p><b>Condition:</b> ${result.condition} ${result.target_price}</p>
                `;

            }

            else{

                div.innerHTML = `
                    <h2 style="color:#f59e0b;">
                        ⏳ Alert Not Triggered
                    </h2>

                    <br>

                    <p><b>Asset:</b> ${result.asset}</p>

                    <p><b>Current Price:</b> $${result.current_price}</p>

                    <p><b>Waiting for:</b> ${result.condition} ${result.target_price}</p>
                `;

            }

        }

        catch(err){

            console.error(err);

            alert("Unable to check alert.");

        }

    });

});