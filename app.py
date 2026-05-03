from flask import Flask, render_template
import sqlite3
import yfinance as yf

app = Flask(__name__)



@app.route("/")
def home():
    verbinding = sqlite3.connect("portfolio.db")
    cursor = verbinding.cursor()
    cursor.execute("SELECT * FROM portfolio")
    resultaat = cursor.fetchall()

    portfolio = []
    
    totaal = 0
    
    for rij in resultaat:
        aandeel = yf.Ticker(rij[2] + ".L")
        live_prijs = round(aandeel.info["navPrice"], 2)
        waarde = round(rij[3] * live_prijs, 2)
        winst_verlies = round(waarde - rij[3] * rij[4], 2)  # Assuming rij[4] is the purchase price
        portfolio.append([rij[1], live_prijs, waarde, winst_verlies])
        totaal = round(totaal + winst_verlies, 2)

    return render_template("index.html", totaal=totaal, portfolio=portfolio)

if __name__ == "__main__":
    app.run(debug=True)