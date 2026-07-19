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

    function updateAssets() {

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

    let chart = null;

    function drawChart(aiEquity, buyHoldEquity) {

        const canvas = document.getElementById("equityChart");

        if(chart){
            chart.destroy();
        }

        chart = new Chart(canvas,{

            type:"line",

            data:{

                labels: aiEquity.map((_,i)=>i+1),

                datasets:[

                    {
                        label:"AI Strategy",
                        data:aiEquity,
                        borderColor:"#22c55e",
                        backgroundColor:"rgba(34,197,94,.15)",
                        borderWidth:3,
                        fill:true,
                        pointRadius:0,
                        tension:.35
                    },

                    {
                        label:"Buy & Hold",
                        data:buyHoldEquity,
                        borderColor:"#3b82f6",
                        backgroundColor:"rgba(59,130,246,.10)",
                        borderWidth:3,
                        fill:false,
                        pointRadius:0,
                        tension:.35
                    }

                ]

            },

            options:{
                responsive:true,
                maintainAspectRatio:false
            }

        });

    }

    function showToast(message,isError=false){

        const toast=document.getElementById("toast");

        if(!toast){
            alert(message);
            return;
        }

        toast.innerHTML=message;

        toast.className=isError
            ? "toast show error"
            : "toast show";

        setTimeout(()=>{
            toast.className="toast";
        },3000);

    }

    document.getElementById("runBacktestBtn").addEventListener("click",async()=>{

        document.getElementById("loadingOverlay").style.display="flex";

        const payload={

            asset:asset.value,
            strategy:document.getElementById("strategy").value,
            capital:document.getElementById("capital").value,
            start_date:document.getElementById("start_date").value,
            end_date:document.getElementById("end_date").value

        };

        try{

            const response=await fetch("/api/backtest",{

                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify(payload)

            });

            const result=await response.json();

            document.getElementById("loadingOverlay").style.display="none";

            if(!result.success){

                showToast(result.message,true);
                return;

            }

            document.getElementById("totalReturn").innerHTML=
                result.total_return.toFixed(2)+"%";

            document.getElementById("sharpeRatio").innerHTML=
                Number(result.sharpe).toFixed(2);

            document.getElementById("maxDrawdown").innerHTML=
                result.drawdown.toFixed(2)+"%";

            document.getElementById("winRate").innerHTML=
                result.win_rate.toFixed(2)+"%";

            if(document.getElementById("aiReturn")){

                document.getElementById("aiReturn").innerHTML=
                    result.total_return.toFixed(2)+"%";

            }

            if(document.getElementById("buyHoldReturn")){

                document.getElementById("buyHoldReturn").innerHTML=
                    result.buy_hold_return.toFixed(2)+"%";

            }

            if(document.getElementById("outperformance")){

                const outperformance=
                    result.total_return-result.buy_hold_return;

                document.getElementById("outperformance").innerHTML=
                    outperformance.toFixed(2)+"%";

            }

            drawChart(
                result.equity,
                result.buy_hold_equity
            );

            const table=document.getElementById("tradeTable");

            table.innerHTML="";

            if(result.trades.length===0){

                table.innerHTML=
                    "<tr><td colspan='4'>No Trades Executed</td></tr>";

            }

            else{

                result.trades.forEach(t=>{

                    table.innerHTML+=`

                    <tr>

                        <td>${t.date}</td>

                        <td style="color:${t.signal==="BUY" ? "#22c55e" : "#ef4444"}">

                            ${t.signal}

                        </td>

                        <td>$${t.price}</td>

                        <td>$${t.portfolio}</td>

                    </tr>

                    `;

                });

            }

            showToast("Backtest Completed Successfully");

        }

        catch(err){

            console.error(err);

            document.getElementById("loadingOverlay").style.display="none";

            showToast("Backtest Failed",true);

        }

    });

});