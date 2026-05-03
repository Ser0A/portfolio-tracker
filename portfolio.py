import sqlite3
import yfinance as yf

verbinding = sqlite3.connect("portfolio.db")
cursor = verbinding.cursor()

cursor.execute("SELECT * FROM portfolio")
resultaat = cursor.fetchall()

totaal = 0

for rij in resultaat:
    aandeel = yf.Ticker(rij[2] + ".L")
    live_prijs = round(aandeel.info["navPrice"], 2) 
    waarde = round(rij[3] * live_prijs, 2)
    winst_verlies = round(waarde - (rij[3] * rij[4]), 2)
    totaal = round(totaal + winst_verlies, 2)
    print(rij[1], "|", "Prijs:", live_prijs, "|", "Waarde:", waarde, "|", "W/V:", winst_verlies)
print("Totaal:", totaal)

import matplotlib.pyplot as plt

namen = []
waardes = []

for rij in resultaat:
    aandeel = yf.Ticker(rij[2] + ".L")
    live_prijs = aandeel.info["navPrice"]
    waarde = rij[3] * live_prijs
    namen.append(rij[1])
    waardes.append(waarde)

plt.pie(waardes, labels=namen, autopct="%1.1f%%")
plt.show()
