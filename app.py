from flask import Flask, jsonify
import yfinance as yf
from apscheduler.schedulers.background import BackgroundScheduler
import threading

app = Flask(__name__)

# List of stock tickers
stocks = [
    "AXISBANK.NS", "AUBANK.NS", "BANDHANBNK.NS", "BANKBARODA.NS", "BANKINDIA.NS",
    "CANBK.NS", "CUB.NS", "FEDERALBNK.NS", "HDFCBANK.NS", "ICICIBANK.NS",
    "IDFCFIRSTB.NS", "INDUSINDBK.NS", "KOTAKBANK.NS", "PNB.NS", "RBLBANK.NS",
    "SBIN.NS", "YESBANK.NS", "ABCAPITAL.NS", "ANGELONE.NS", "BAJFINANCE.NS",
    "BAJAJFINSV.NS", "CANFINHOME.NS", "CHOLAFIN.NS", "HDFCAMC.NS", "HDFCLIFE.NS",
    "ICICIGI.NS", "ICICIPRULI.NS", "LICIHSGFIN.NS", "M&MFIN.NS", "MANAPPURAM.NS",
    "MUTHOOTFIN.NS", "PEL.NS", "PFC.NS", "POONAWALLA.NS", "RECLTD.NS", "SBICARD.NS",
    "SBILIFE.NS", "SHRIRAMFIN.NS", "ADANIGREEN.NS", "ADANIPORTS.NS", "BPCL.NS",
    "GAIL.NS", "GUJGASLTD.NS", "IGL.NS", "IOC.NS", "MGL.NS", "NTPC.NS", "OIL.NS",
    "ONGC.NS", "PETRONET.NS", "POWERGRID.NS", "RELIANCE.NS", "SJVN.NS", "TATAPOWER.NS",
    "ADANIENSOL.NS", "NHPC.NS", "NTPC.NS", "POWERGRID.NS", "SJVN.NS", "TATAPOWER.NS",
    "ACC.NS", "AMBUJACEM.NS", "DALBHARAT.NS", "JKCEMENT.NS", "RAMCOCEM.NS", "SHREECEM.NS",
    "ULTRACEMCO.NS", "APLAPOLLO.NS", "HINDALCO.NS", "HINDCOPPER.NS", "JINDALSTEL.NS",
    "JSWSTEEL.NS", "NATIONALUM.NS", "NMDC.NS", "SAIL.NS", "TATASTEEL.NS", "VEDL.NS",
    "BSOFT.NS", "COFORGE.NS", "CYIENT.NS", "INFY.NS", "LTIM.NS", "LTTS.NS", "MPHASIS.NS",
    "PERSISTENT.NS", "TATAELXSI.NS", "TCS.NS", "TECHM.NS", "WIPRO.NS", "ASHOKLEY.NS",
    "BAJAJ-AUTO.NS", "BHARATFORG.NS", "EICHERMOT.NS", "HEROMOTOCO.NS", "M&M.NS",
    "MARUTI.NS", "MOTHERSON.NS", "TATAMOTORS.NS", "TVSMOTOR.NS", "ABFRL.NS", "DMART.NS",
    "NYKAA.NS", "PAGEIND.NS", "PAYTM.NS", "TRENT.NS", "VBL.NS", "ZOMATO.NS", "ASIANPAINT.NS",
    "BERGEPAINT.NS", "BRITANNIA.NS", "COLPAL.NS", "DABUR.NS", "GODREJCP.NS", "HINDUNILVR.NS",
    "ITC.NS", "MARICO.NS", "NESTLEIND.NS", "TATACONSUM.NS", "UBL.NS", "UNITEDSPR.NS",
    "VOLTAS.NS", "ALKEM.NS", "APLLTD.NS", "AUROPHARMA.NS", "BIOCON.NS", "CIPLA.NS",
    "DIVISLAB.NS", "DRREDDY.NS", "GLENMARK.NS", "GRANULES.NS", "LAURUSLABS.NS", "LUPIN.NS",
    "SUNPHARMA.NS", "SYNGENE.NS", "TORNTPHARM.NS", "APOLLOHOSP.NS", "LALPATHLAB.NS",
    "MAXHEALTH.NS", "METROPOLIS.NS", "BHARTIARTL.NS", "HFCL.NS", "IDEA.NS", "INDUSTOWER.NS",
    "DLF.NS", "GODREJPROP.NS", "LODHA.NS", "OBEROIRLTY.NS", "PRESTIGE.NS", "GUJGASLTD.NS",
    "IGL.NS", "MGL.NS", "CONCOR.NS", "CESC.NS", "HUDCO.NS", "IRFC.NS", "ABBOTINDIA.NS",
    "BEL.NS", "CGPOWER.NS", "CUMMINSIND.NS", "HAL.NS", "L&T.NS", "SIEMENS.NS", "TIINDIA.NS",
    "CHAMBLFERT.NS", "COROMANDEL.NS", "GNFC.NS", "PIIND.NS", "BSE.NS", "DELHIVERY.NS",
    "GMRAIRPORT.NS", "IRCTC.NS", "KEI.NS", "NAVINFLUOR.NS", "POLYCAB.NS", "SUNTV.NS", "UPL.NS"
]

# Store stock data
stock_data = {}

def fetch_stock_data():
    """Fetch stock data and update the global stock_data dictionary."""
    global stock_data
    print("Fetching stock data...")
    new_data = {}
    
    for stock in stocks:
        try:
            ticker = yf.Ticker(stock)
            hist = ticker.history(period="1d")
            if not hist.empty:
                last_close = hist['Close'].iloc[-1]
                new_data[stock] = {"price": last_close}
        except Exception as e:
            print(f"Error fetching {stock}: {e}")
    
    stock_data = new_data  # Update the global stock data
    print("Stock data updated.")

# Run the fetch function initially
fetch_stock_data()

# Scheduler to update stock data every 5 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(fetch_stock_data, "interval", minutes=5)
scheduler.start()

@app.route("/stocks", methods=["GET"])
def get_stocks():
    """API endpoint to get all stock prices."""
    return jsonify(stock_data)

if __name__ == "__main__":
    # Run Flask app with threading enabled
    app.run(host="0.0.0.0", port=5000, threaded=True)
