const assets = {

    "Stocks": [
        "AAPL",
        "MSFT",
        "NVDA",
        "GOOGL",
        "META",
        "AMZN",
        "TSLA"
    ],

    "Crypto": [
        "BTC-USD",
        "ETH-USD",
        "SOL-USD",
        "BNB-USD",
        "XRP-USD"
    ],

    "Forex": [
        "EURUSD=X",
        "GBPUSD=X",
        "USDJPY=X",
        "USDINR=X"
    ],

    "Indices": [
        "^GSPC",
        "^IXIC",
        "^DJI",
        "^NSEI",
        "^NSEBANK"
    ],

    "Commodities": [
        "GC=F",
        "SI=F",
        "CL=F",
        "NG=F"
    ]

};


document.addEventListener("DOMContentLoaded", () => {

    const assetClass = document.getElementById("asset_class");
    const asset = document.getElementById("asset");

    assetClass.addEventListener("change", () => {

        const selected = assetClass.value;

        asset.innerHTML = "";

        assets[selected].forEach(item => {

            const option = document.createElement("option");

            option.value = item;
            option.textContent = item;

            asset.appendChild(option);

        });

    });

});