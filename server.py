import os
from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf

app = Flask(__name__)
CORS(app)  # 允許跨網域存取

STOCKS = {
    # ETF 清單
    '0050': '0050.TW',
    '0056': '0056.TW',
    '00878': '00878.TW',
    '00713': '00713.TW',
    '00929': '00929.TW',
    '00940': '00940.TW',
    '00939': '00939.TW',
    '00919': '00919.TW',
    '00981A': '00981A.TW',
    '00982A': '00982A.TW',
    # 金融股
    '5880': '5880.TW',
    '2885': '2885.TW',
    '2887': '2887.TW',
    '2891': '2891.TW',
    '2886': '2886.TW',
    '2880': '2880.TW',
    '2884': '2884.TW',
    # 電子 / 科技股
    '2317': '2317.TW',
    '2498': '2498.TW',
    '2368': '2368.TW',
    '2330': '2330.TW',
    '3481': '3481.TW',
    '2409': '2409.TW',
    '2337': '2337.TW',
    '2408': '2408.TW',
    '2344': '2344.TW',
    '6770': '6770.TW',
    '2303': '2303.TW',
    '3008': '3008.TW',
    '2454': '2454.TW',
    '3037': '3037.TW',
    '2449': '2449.TW'
}

@app.route('/api/stocks')
def get_stocks():
    result = []
    for code, ticker_symbol in STOCKS.items():
        try:
            ticker = yf.Ticker(ticker_symbol)
            hist = ticker.history(period='5d')
            
            if len(hist) >= 1:
                last_row = hist.iloc[-1]
                price = round(float(last_row['Close']), 2)
                high = round(float(last_row['High']), 2)
                low = round(float(last_row['Low']), 2)
                volume = int(last_row['Volume'])
                
                if len(hist) >= 2:
                    prev_close = float(hist.iloc[-2]['Close'])
                    change = round(price - prev_close, 2)
                    change_pct = round((change / prev_close) * 100, 2)
                else:
                    change = 0.0
                    change_pct = 0.0
            else:
                price = high = low = volume = change = change_pct = None

            result.append({
                'symbol': code,
                'price': price,
                'change': change,
                'change_pct': change_pct,
                'high': high,
                'low': low,
                'volume': volume
            })
        except Exception as e:
            print(f"抓取 {code} 失敗: {e}")
            result.append({
                'symbol': code, 
                'price': None, 
                'change': 0.0, 
                'change_pct': 0.0, 
                'high': None, 
                'low': None, 
                'volume': 0
            })
            
    return jsonify(result)

if __name__ == '__main__':
    # 支援 Render 指定的 PORT 變數
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)