import yfinance as yf
from flask import Flask, jsonify

app = Flask(__name__)

# List of Indian stocks for fetching data
indian_stocks = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ACC.NS",
    "APLAPOLLO.NS", "AUBANK.NS", "AARTIIND.NS", "ABBOTINDIA.NS",
    "ADANIENSOL.NS", "ADANIENT.NS", "ADANIGREEN.NS", "ADANIPORTS.NS",
    "ATGL.NS", "ABCAPITAL.NS", "ABFRL.NS", "ALKEM.NS", "AMBUJACEM.NS",
    "ANGELONE.NS", "APOLLOHOSP.NS", "APOLLOTYRE.NS", "ASHOKLEY.NS",
    "ASIANPAINT.NS", "ASTRAL.NS", "ATUL.NS", "AUROPHARMA.NS", "DMART.NS",
    "AXISBANK.NS", "BSOFT.NS", "BSE.NS", "BAJAJ-AUTO.NS", "BAJFINANCE.NS",
    "BAJAJFINSV.NS", "BALKRISIND.NS", "BANDHANBNK.NS", "BANKBARODA.NS",
    "BANKINDIA.NS", "BATAINDIA.NS", "BERGEPAINT.NS", "BEL.NS", "BHARATFORG.NS",
    "BHEL.NS", "BPCL.NS", "BHARTIARTL.NS", "BIOCON.NS", "BOSCHLTD.NS",
    "BRITANNIA.NS", "CESC.NS", "CGPOWER.NS", "CANFINHOME.NS", "CANBK.NS",
    "CDSL.NS", "CHAMBLFERT.NS", "CHOLAFIN.NS", "CIPLA.NS", "CUB.NS",
    "COALINDIA.NS", "COFORGE.NS", "COLPAL.NS", "CAMS.NS", "CONCOR.NS",
    "COROMANDEL.NS", "CROMPTON.NS", "CUMMINSIND.NS", "CYIENT.NS", "DLF.NS",
    "DABUR.NS", "DALBHARAT.NS", "DEEPAKNTR.NS", "DELHIVERY.NS", "DIVISLAB.NS",
    "DIXON.NS", "LALPATHLAB.NS", "DRREDDY.NS", "EICHERMOT.NS", "ESCORTS.NS",
    "EXIDEIND.NS", "NYKAA.NS", "GAIL.NS", "GMRAIRPORT.NS", "GLENMARK.NS",
    "GODREJCP.NS", "GODREJPROP.NS", "GRANULES.NS", "GRASIM.NS", "GUJGASLTD.NS",
    "GNFC.NS", "HCLTECH.NS", "HDFCAMC.NS", "HDFCLIFE.NS", "HFCL.NS",
    "HAVELLS.NS", "HEROMOTOCO.NS", "HINDALCO.NS", "HAL.NS", "HINDCOPPER.NS",
    "HINDPETRO.NS", "HINDUNILVR.NS", "HUDCO.NS", "ICICIBANK.NS", "ICICIGI.NS",
    "ICICIPRULI.NS", "IDFCFIRSTB.NS", "IPCALAB.NS", "IRB.NS", "ITC.NS",
    "INDIAMART.NS", "INDIANB.NS", "IEX.NS", "IOC.NS", "IRCTC.NS", "IRFC.NS",
    "IGL.NS", "INDUSTOWER.NS", "INDUSINDBK.NS", "NAUKRI.NS", "INFY.NS",
    "INDIGO.NS", "JKCEMENT.NS", "JSWENERGY.NS", "JSWSTEEL.NS", "JSL.NS",
    "JINDALSTEL.NS", "JIOFIN.NS", "JUBLFOOD.NS", "KEI.NS", "KPITTECH.NS",
    "KALYANKJIL.NS", "KOTAKBANK.NS", "LTF.NS", "LTTS.NS", "LICHSGFIN.NS",
    "LTIM.NS", "LT.NS", "LAURUSLABS.NS", "LICI.NS", "LUPIN.NS", "MRF.NS",
    "LODHA.NS", "MGL.NS", "M&MFIN.NS", "M&M.NS", "MANAPPURAM.NS", "MARICO.NS",
    "MARUTI.NS", "MFSL.NS", "MAXHEALTH.NS", "METROPOLIS.NS", "MPHASIS.NS",
    "MCX.NS", "MUTHOOTFIN.NS", "NCC.NS", "NHPC.NS", "NMDC.NS", "NTPC.NS",
    "NATIONALUM.NS", "NAVINFLUOR.NS", "NESTLEIND.NS", "OBEROIRLTY.NS", "ONGC.NS",
    "OIL.NS", "PAYTM.NS", "OFSS.NS", "POLICYBZR.NS", "PIIND.NS", "PVRINOX.NS",
    "PAGEIND.NS", "PERSISTENT.NS", "PETRONET.NS", "PIDILITIND.NS", "PEL.NS",
    "POLYCAB.NS", "POONAWALLA.NS", "PFC.NS", "POWERGRID.NS", "PRESTIGE.NS",
    "PNB.NS", "RBLBANK.NS", "RECLTD.NS", "RELIANCE.NS", "SBICARD.NS", "SBILIFE.NS",
    "SHREECEM.NS", "SJVN.NS", "SRF.NS", "MOTHERSON.NS", "SHRIRAMFIN.NS", "SIEMENS.NS",
    "SONACOMS.NS", "SBIN.NS", "SAIL.NS", "SUNPHARMA.NS", "SUNTV.NS", "SUPREMEIND.NS",
    "SYNGENE.NS", "TATACONSUM.NS", "TVSMOTOR.NS", "TATACHEM.NS", "TATACOMM.NS",
    "TCS.NS", "TATAELXSI.NS", "TATAMOTORS.NS", "TATAPOWER.NS", "TATASTEEL.NS",
    "TECHM.NS", "FEDERALBNK.NS", "INDHOTEL.NS", "RAMCOCEM.NS", "TITAN.NS",
    "TORNTPHARM.NS", "TRENT.NS", "TIINDIA.NS", "UPL.NS", "ULTRACEMCO.NS",
    "UNIONBANK.NS", "UBL.NS", "UNITDSPR.NS", "VBL.NS", "VEDL.NS", "IDEA.NS",
    "VOLTAS.NS", "WIPRO.NS", "YESBANK.NS", "ZOMATO.NS"
]

# Function to fetch stock data
def fetch_stock_data(stocks):
    stock_data = {}
    for stock in stocks:
        data = yf.Ticker(stock).history(period="5d")  # Fetch last 5 days data
        if not data.empty:
            prev_close = data['Close'].iloc[-2]  # Second last day's close (previous day)
            current_price = data['Close'].iloc[-1]  # Last day's price (current day)
            percentage_change = ((current_price - prev_close) / prev_close) * 100  # Percentage change
            stock_data[stock] = {
                'previous_close': prev_close,
                'current_price': current_price,
                'percentage_change': percentage_change
            }
    return stock_data

# Endpoint to get all gainers
@app.route('/gainers', methods=['GET'])
def gainers():
    stock_data = fetch_stock_data(indian_stocks)

    # Separate gainers
    gainers = {stock: data for stock, data in stock_data.items() if data['percentage_change'] > 0}

    # Sort gainers by percentage change in descending order
    sorted_gainers = sorted(gainers.items(), key=lambda x: x[1]['percentage_change'], reverse=True)

    return jsonify(sorted_gainers)

# Endpoint to get all losers
@app.route('/losers', methods=['GET'])
def losers():
    stock_data = fetch_stock_data(indian_stocks)

    # Separate losers
    losers = {stock: data for stock, data in stock_data.items() if data['percentage_change'] < 0}

    # Sort losers by percentage change in ascending order
    sorted_losers = sorted(losers.items(), key=lambda x: x[1]['percentage_change'])

    return jsonify(sorted_losers)

# Running the Flask app
if __name__ == '__main__':
    app.run(debug=True)
