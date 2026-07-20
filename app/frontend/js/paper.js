document.addEventListener("DOMContentLoaded", () => {

    const portfolioDiv = document.getElementById("portfolio");
    const historyDiv = document.getElementById("historyTable");

    async function loadPortfolio() {

        try {

            const response = await fetch("/api/paper");
            const portfolio = await response.json();

            // ==========================
            // ANALYTICS
            // ==========================

            document.getElementById("cash").innerHTML =
                "$" + portfolio.cash.toFixed(2);

            document.getElementById("portfolioValue").innerHTML =
                "$" + portfolio.portfolio_value.toFixed(2);

            document.getElementById("pnl").innerHTML =
                "$" + portfolio.unrealized.toFixed(2);

            document.getElementById("returnPct").innerHTML =
                portfolio.return_pct.toFixed(2) + "%";

            // ==========================
            // POSITIONS COUNT
            // ==========================

            document.getElementById("posCount").innerHTML =
                portfolio.positions;


            // ==========================
            // OPEN POSITIONS
            // ==========================

            let html = "";

            if (portfolio.holdings.length === 0) {

                html = `
                <div style="text-align:center;padding:30px;color:#888;">
                    No Open Positions
                </div>
                `;

            } else {

                html = `
                <table class="table">

                    <tr>

                        <th>Asset</th>

                        <th>Quantity</th>

                        <th>Buy Price</th>

                        <th>Current Price</th>

                        <th>Market Value</th>

                        <th>P/L</th>

                    </tr>
                `;

                portfolio.holdings.forEach(position => {

                    html += `

                    <tr>

                        <td>${position.asset}</td>

                        <td>${position.quantity}</td>

                        <td>$${position.buy_price.toFixed(2)}</td>

                        <td>$${position.current_price.toFixed(2)}</td>

                        <td>$${position.market_value.toFixed(2)}</td>

                        <td style="color:${position.unrealized >= 0 ? "#22c55e" : "#ef4444"}">

                            $${position.unrealized.toFixed(2)}

                        </td>

                    </tr>

                    `;

                });

                html += "</table>";
            }

            portfolioDiv.innerHTML = html;

            // ==========================
            // TRADE HISTORY
            // ==========================

            let historyHtml = "";

            if (!portfolio.history || portfolio.history.length === 0) {

                historyHtml = "<p>No Trades Yet</p>";

            } else {

                historyHtml = `
                <table class="table">

                    <tr>
                        <th>Date</th>
                        <th>Asset</th>
                        <th>Action</th>
                        <th>Qty</th>
                        <th>Price</th>
                        <th>Total</th>
                    </tr>
                `;

                portfolio.history.forEach(trade => {

                    historyHtml += `
                    <tr>

                        <td>${trade.date}</td>

                        <td>${trade.asset}</td>

                        <td style="color:${trade.action === "BUY" ? "#22c55e" : "#ef4444"}">
                            ${trade.action}
                        </td>

                        <td>${trade.quantity}</td>

                        <td>$${Number(trade.price).toFixed(2)}</td>

                        <td>$${Number(trade.total).toFixed(2)}</td>

                    </tr>
                    `;

                });

                historyHtml += "</table>";
            }

            historyDiv.innerHTML = historyHtml;

        }

        catch (err) {

            console.error(err);

            portfolioDiv.innerHTML = "<p>Unable to load portfolio.</p>";

            historyDiv.innerHTML = "<p>Unable to load history.</p>";

        }

    }

    // ==========================
    // LIVE PRICE + ESTIMATED VALUE
    // ==========================

    async function updatePrice() {

        const asset = document.getElementById("asset").value;
        const qty = Number(document.getElementById("quantity").value);

        try {

            const res = await fetch(`/api/live-price/${asset}`);

            const data = await res.json();

            if (!data.success) {

                document.getElementById("livePrice").value = "-";
                document.getElementById("estValue").value = "-";
                return;

            }

            document.getElementById("livePrice").value =
                "$" + data.price.toFixed(2);

            document.getElementById("estValue").value =
                "$" + (data.price * qty).toFixed(2);

        }

        catch (err) {

            document.getElementById("livePrice").value = "-";
            document.getElementById("estValue").value = "-";

        }

    }

    // Initial Load
    loadPortfolio();
    updatePrice();

    // Update price whenever asset or quantity changes
    document.getElementById("asset").addEventListener("change", updatePrice);
    document.getElementById("quantity").addEventListener("input", updatePrice);

    // ==========================
    // BUY
    // ==========================

    document.getElementById("buyBtn").addEventListener("click", async () => {

        const payload = {

            asset: document.getElementById("asset").value,

            quantity: Number(document.getElementById("quantity").value)

        };

        try {

            const response = await fetch("/api/paper/buy", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(payload)

            });

            const result = await response.json();

            alert(result.message);

            await loadPortfolio();
            await updatePrice();

        }

        catch (err) {

            console.error(err);

            alert("Unable to execute BUY order.");

        }

    });

    // ==========================
    // SELL
    // ==========================

    document.getElementById("sellBtn").addEventListener("click", async () => {

        const payload = {

            asset: document.getElementById("asset").value,

            quantity: Number(document.getElementById("quantity").value)

        };

        try {

            const response = await fetch("/api/paper/sell", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(payload)

            });

            const result = await response.json();

            alert(result.message);

            await loadPortfolio();
            await updatePrice();

        }

        catch (err) {

            console.error(err);

            alert("Unable to execute SELL order.");

        }

    });

});