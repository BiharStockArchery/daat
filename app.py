import os
import yfinance as yf
from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler

# Define your Flask app
app = Flask(__name__)

# Define your global variable to store the stock data
stock_data = {}  # Store fetched stock data globally

# List of all stocks (your list of stocks remains unchanged)
all_stocks = [
    "AXISBANK.NS", "AUBANK.NS", "BANDHANBNK.NS", "BANKBARODA.NS", "BANKINDIA.NS",
    "CANBK.NS", "CUB.NS", "FEDERALBNK.NS", "HDFCBANK.NS", "ICICIBANK.NS", "IDFCFIRSTB.NS",
    "INDUSINDBK.NS", "KOTAKBANK.NS", "PNB.NS", "RBLBANK.NS", "SBIN.NS", "YESBANK.NS",
    "ABCAPITAL.NS", "ANGELONE.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", "CANFINHOME.NS",
    "CHOLAFIN.NS", "HDFCAMC.NS", "HDFCLIFE.NS", "ICICIGI.NS", "ICICIPRULI.NS", "LICIHSGFIN.NS",
    "M&MFIN.NS", "MANAPPURAM.NS", "MUTHOOTFIN.NS", "PEL.NS", "PFC.NS", "POONAWALLA.NS",
    "RECLTD.NS", "SBICARD.NS", "SBILIFE.NS", "SHRIRAMFIN.NS", "ADANIGREEN.NS", "ADANIPORTS.NS",
    "BPCL.NS", "GAIL.NS", "GUJGASLTD.NS", "IGL.NS", "IOC.NS", "MGL.NS", "NTPC.NS", "OIL.NS",
    "ONGC.NS", "PETRONET.NS", "POWERGRID.NS", "RELIANCE.NS", "SJVN.NS", "TATAPOWER.NS",
    "ADANIENSOL.NS", "NHPC.NS", "NTPC.NS", "POWERGRID.NS", "SJVN.NS", "TATAPOWER.NS",
    "ACC.NS", "AMBUJACEM.NS", "DALBHARAT.NS", "JKCEMENT.NS", "RAMCOCEM.NS", "SHREECEM.NS",
    "ULTRACEMCO.NS", "APLAPOLLO.NS", "HINDALCO.NS", "HINDCOPPER.NS", "JINDALSTEL.NS", "JSWSTEEL.NS",
    "NATIONALUM.NS", "NMDC.NS", "SAIL.NS", "TATASTEEL.NS", "VEDL.NS", "BSOFT.NS", "COFORGE.NS",
    "CYIENT.NS", "INFY.NS", "LTIM.NS", "LTTS.NS", "MPHASIS.NS", "PERSISTENT.NS", "TATAELXSI.NS",
    "TCS.NS", "TECHM.NS", "WIPRO.NS", "ASHOKLEY.NS", "BAJAJ-AUTO.NS", "BHARATFORG.NS", "EICHERMOT.NS",
    "HEROMOTOCO.NS", "M&M.NS", "MARUTI.NS", "MOTHERSON.NS", "TATAMOTORS.NS", "TVSMOTOR.NS",
    "ABFRL.NS", "DMART.NS", "NYKAA.NS", "PAGEIND.NS", "PAYTM.NS", "TRENT.NS", "VBL.NS", "ZOMATO.NS",
    "ASIANPAINT.NS", "BERGEPAINT.NS", "BRITANNIA.NS", "COLPAL.NS", "DABUR.NS", "GODREJCP.NS", 
    "HINDUNILVR.NS", "ITC.NS", "MARICO.NS", "NESTLEIND.NS", "TATACONSUM.NS", "UBL.NS", "UNITEDSPR.NS", 
    "VOLTAS.NS", "ALKEM.NS", "APLLTD.NS", "AUROPHARMA.NS", "BIOCON.NS", "CIPLA.NS", "DIVISLAB.NS",
    "DRREDDY.NS", "GLENMARK.NS", "GRANULES.NS", "LAURUSLABS.NS", "LUPIN.NS", "SUNPHARMA.NS",
    "SYNGENE.NS", "TORNTPHARM.NS", "APOLLOHOSP.NS", "LALPATHLAB.NS", "MAXHEALTH.NS", "METROPOLIS.NS",
    "BHARTIARTL.NS", "HFCL.NS", "IDEA.NS", "INDUSTOWER.NS", "DLF.NS", "GODREJPROP.NS", "LODHA.NS",
    "OBEROIRLTY.NS", "PRESTIGE.NS", "GUJGASLTD.NS", "IGL.NS", "MGL.NS", "CONCOR.NS", "CESC.NS", 
    "HUDCO.NS", "IRFC.NS", "ABBOTINDIA.NS", "BEL.NS", "CGPOWER.NS", "CUMMINSIND.NS", "HAL.NS", 
    "L&T.NS", "SIEMENS.NS", "TIINDIA.NS", "CHAMBLFERT.NS", "COROMANDEL.NS", "GNFC.NS", "PIIND.NS", 
    "BSE.NS", "DELHIVERY.NS", "GMRAIRPORT.NS", "IRCTC.NS", "KEI.NS", "NAVINFLUOR.NS", "POLYCAB.NS",
    "SUNTV.NS", "UPL.NS"
]

# Function to fetch stock data from Yahoo Finance
def get_stock_data(stock_list):
    stock_data = {}
    for stock in stock_list:
        try:
            data = yf.Ticker(stock).history(period="1d")
            stock_data[stock] = {
                "current_price": data['Close'].iloc[-1],
                "change": data['Close'].pct_change().iloc[-1] * 100  # percentage change
            }
        except Exception as e:
            print(f"Error fetching data for {stock}: {e}")
            stock_data[stock] = {"error": "Failed to fetch data"}
    return stock_data

# Function to update stock data every 2 minutes
def update_stock_data():
    global stock_data
    stock_data = get_stock_data(all_stocks)
    print("Stock data updated!")

# Initialize APScheduler to run the task periodically
scheduler = BackgroundScheduler()
scheduler.add_job(update_stock_data, 'interval', minutes=2)
scheduler.start()

# Fetch stock data when the app starts
update_stock_data()

# Flask route to fetch gainers
@app.route('/gainers', methods=['GET'])
def get_gainers():
    try:
        # Filter gainers (stocks with positive change)
        gainers = {stock: data for stock, data in stock_data.items() if "change" in data and data["change"] > 0}
        return jsonify(gainers)
    except Exception as e:
        print(f"Error fetching gainers: {e}")
        return jsonify({"error": "Failed to fetch gainers data"}), 500

# Flask route to fetch losers
@app.route('/losers', methods=['GET'])
def get_losers():
    try:
        # Filter losers (stocks with negative change)
        losers = {stock: data for stock, data in stock_data.items() if "change" in data and data["change"] < 0}
        return jsonify(losers)
    except Exception as e:
        print(f"Error fetching losers: {e}")
        return jsonify({"error": "Failed to fetch losers data"}), 500

if __name__ == "__main__":
    # Ensure the app runs on the right host and port for Railway
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)
