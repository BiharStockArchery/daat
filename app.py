import os
from flask import Flask, jsonify
import yfinance as yf
from apscheduler.schedulers.background import BackgroundScheduler
from threading import Lock

app = Flask(__name__)

# List of all stocks
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
    "ONGC.NS", "PETRONET.NS", "POWERGRID.NS", "RELIANCE.NS", "SJVN.NS", "TATAPOWER.NS"
]

# Global dictionary to store stock data
stock_cache = {}
cache_lock = Lock()

# Function to fetch stock data from yfinance
def fetch_stock_data():
    global stock_cache
    try:
        # Use yf.download() for better efficiency (fetches all stocks in one request)
        data = yf.download(all_stocks, period="5d", group_by="ticker")
        new_stock_cache = {}

        for stock in all_stocks:
            try:
                if stock in data and not data[stock].empty:
                    previous_close = data[stock]['Close'].iloc[-2]  # 2nd last day close
                    current_price = data[stock]['Close'].iloc[-1]  # Most recent close
                    change = ((current_price - previous_close) / previous_close) * 100  # Percentage change

                    new_stock_cache[stock] = {
                        "current_price": round(current_price, 2),
                        "previous_close": round(previous_close, 2),
                        "change": round(change, 2)
                    }
            except Exception as e:
                print(f"Error processing data for {stock}: {e}")

        # Update stock cache with thread safety
        with cache_lock:
            stock_cache = new_stock_cache
        print("Stock data updated.")

    except Exception as e:
        print(f"Error fetching stock data: {e}")

# Scheduler to update stock data every 10 seconds
scheduler = BackgroundScheduler()
scheduler.add_job(fetch_stock_data, 'interval', seconds=10)
scheduler.start()

# API endpoint to get gainers
@app.route('/gainers', methods=['GET'])
def get_gainers():
    with cache_lock:
        gainers = {stock: data for stock, data in stock_cache.items() if data["change"] > 0}
    return jsonify(gainers)

# API endpoint to get losers
@app.route('/losers', methods=['GET'])
def get_losers():
    with cache_lock:
        losers = {stock: data for stock, data in stock_cache.items() if data["change"] < 0}
    return jsonify(losers)

# API endpoint to get all stock data
@app.route('/stocks', methods=['GET'])
def get_all_stocks():
    with cache_lock:
        return jsonify(stock_cache)

if __name__ == '__main__':
    # Fetch initial stock data before starting the server
    fetch_stock_data()
    app.run(debug=True, use_reloader=False)
