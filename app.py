import os
from flask import Flask, jsonify
import yfinance as yf
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# List of all stocks (same as the one you've provided)
all_stocks = [
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

# Function to fetch stock data from yfinance
def get_stock_data(stock_list):
    stock_data = {}
    for stock in stock_list:
        try:
            ticker = yf.Ticker(stock)
            data = ticker.history(period="5d")  # Fetch data for the last 5 days
            if not data.empty:
                # Get the previous close and the most recent closing price
                previous_close = data['Close'].iloc[-2]  # 2nd last day close
                current_price = data['Close'].iloc[-1]  # Most recent close
                change = ((current_price - previous_close) / previous_close) * 100  # Calculate the percentage change
                stock_data[stock] = {
                    "current_price": current_price,
                    "previous_close": previous_close,
                    "change": change
                }
        except Exception as e:
            print(f"Error fetching data for {stock}: {e}")
            stock_data[stock] = {"current_price": None, "previous_close": None, "change": None}
    return stock_data

# Scheduler function to update stock data every 10 seconds
def update_stock_data():
    stock_data = get_stock_data(all_stocks)
    print("Stock data updated:", stock_data)

# Set up the scheduler to run every 10 seconds
scheduler = BackgroundScheduler()
scheduler.add_job(update_stock_data, 'interval', seconds=60)
scheduler.start()

# Endpoint to get the stock data for gainers
@app.route('/gainers', methods=['GET'])
def get_gainers():
    try:
        stock_data = get_stock_data(all_stocks)
        gainers = {stock: data for stock, data in stock_data.items() if data["change"] > 0}
        return jsonify(gainers)
    except Exception as e:
        print(f"Error fetching gainers data: {e}")
        return jsonify({"error": "Failed to fetch data"}), 500

# Endpoint to get the stock data for losers
@app.route('/losers', methods=['GET'])
def get_losers():
    try:
        stock_data = get_stock_data(all_stocks)
        losers = {stock: data for stock, data in stock_data.items() if data["change"] < 0}
        return jsonify(losers)
    except Exception as e:
        print(f"Error fetching losers data: {e}")
        return jsonify({"error": "Failed to fetch data"}), 500

if __name__ == '__main__':
    # Use the environment variable for the port and bind to 0.0.0.0
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
