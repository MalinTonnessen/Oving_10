import csv
import matplotlib.pyplot as plt
from datetime import datetime

datoer = []
temperaturer = []
snødatoer = []
snødybder = []
nedbørdatoer = []
nedbørverdier = []
vinddatoer = []
vindverdier = []






#Oppgave b 
filnavn = "oslo_blindern_1954_2025_med_makstemperatur.csv" 

antall_dager = {}

with open(filnavn, encoding="utf-8-sig") as fil:
    leser = csv.DictReader(fil, delimiter=";")

    for rad in leser:
        dato = rad["Tid(norsk normaltid)"]
        temperatur = rad["Maksimumstemperatur (døgn)"]

        if temperatur != "":
            temperatur = float(temperatur.replace(",", "."))
            aar = int(dato.split(".")[2])

            if aar not in antall_dager:
                antall_dager[aar] = [0, 0, 0]

            if temperatur > 20:
                antall_dager[aar][0] += 1

            if temperatur > 25:
                antall_dager[aar][1] += 1

            if temperatur > 30:
                antall_dager[aar][2] += 1

aar = int(input("Skriv inn et årstall: "))

if aar in antall_dager:
    sommer, hoysommer, trope = antall_dager[aar]

    print()
    print("Resultater for", aar)
    print("Sommerdager:", sommer)
    print("Høysommerdager:", hoysommer)
    print("Tropedager:", trope)

else:
    print("Fant ingen temperaturdata for dette året.")


# Oppgave c
filer = {
    "Oslo Blindern": "oslo_blindern_1954_2025_med_makstemperatur.csv",
    "Røros": "roeros_1954_2025_med_makstemperatur.csv",
    "Tromsø": "tromsoe_1954_2025_med_makstemperatur 2.csv",
    "Værnes": "vaernes_1954_2025_med_makstemperatur.csv",
    "Venabu": "venabu_1954_2025_med_makstemperatur.csv",
    "Sinnes": "sinnes_2014_2025_med_makstemperatur.csv"
}

def finn_gjennomsnitt(filnavn):
    temperaturer_per_aar = {}

    with open(filnavn, encoding="utf-8-sig") as fil:
        leser = csv.DictReader(fil, delimiter=";")

        for rad in leser:
            dato = rad["Tid(norsk normaltid)"]
            temperatur = rad["Middeltemperatur (døgn)"]

            if temperatur != "" and temperatur != "-":
                aar = int(dato.split(".")[2])
                temperatur = float(temperatur.replace(",", "."))

                if aar not in temperaturer_per_aar:
                    temperaturer_per_aar[aar] = []

                temperaturer_per_aar[aar].append(temperatur)

    gjennomsnitt_per_aar = {}

    for aar in temperaturer_per_aar:
        temperaturer = temperaturer_per_aar[aar]

        if len(temperaturer) >= 300:
            gjennomsnitt = sum(temperaturer) / len(temperaturer)
            gjennomsnitt_per_aar[aar] = gjennomsnitt

    return gjennomsnitt_per_aar

for stasjon, filnavn in filer.items():
    gjennomsnitt = finn_gjennomsnitt(filnavn)

    aarstall = sorted(gjennomsnitt)
    temperaturer = [gjennomsnitt[aar] for aar in aarstall]

    plt.plot(aarstall, temperaturer, label=stasjon)

plt.xlabel("År")
plt.ylabel("Gjennomsnittstemperatur (°C)")
plt.title("Årlig gjennomsnittstemperatur for værstasjoner")
plt.legend()
plt.grid(True)
plt.show()


# Oppgave e – Antall dager med skiføre

import csv
import datetime as dt
import matplotlib.pyplot as plt

# CSV-filene fra oppgave c
filer = {
    "Oslo Blindern": "oslo_blindern_1954_2025_med_makstemperatur.csv",
    "Røros": "roeros_1954_2025_med_makstemperatur.csv",
    "Tromsø": "tromsoe_1954_2025_med_makstemperatur 2.csv",
    "Værnes": "vaernes_1954_2025_med_makstemperatur.csv",
    "Venabu": "venabu_1954_2025_med_makstemperatur.csv",
    "Sinnes": "sinnes_2014_2025_med_makstemperatur.csv"
}


def finn_skidager(filnavn):
    sesonger = {}

    with open(filnavn, encoding="utf-8-sig") as fil:
        leser = csv.DictReader(fil, delimiter=";")

        for rad in leser:
            dato_tekst = rad["Tid(norsk normaltid)"].strip()

            if dato_tekst == "":
                continue

            dato = dt.datetime.strptime(
                dato_tekst, "%d.%m.%Y"
            ).date()

            # Skisesongen er november til mai
            if dato.month not in [11, 12, 1, 2, 3, 4, 5]:
                continue

            snodybde = rad["Snødybde"].strip().replace(",", ".")

            # Hopp over manglende snømålinger
            if snodybde == "" or snodybde == "-":
                continue

            # Finn hvilken skisesong datoen tilhører
            if dato.month >= 11:
                aar = dato.year + 1
            else:
                aar = dato.year

            if aar not in sesonger:
                sesonger[aar] = {}

            sesonger[aar][dato] = float(snodybde)

    resultat = {}

    for aar, maalinger in sesonger.items():

        start = dt.date(aar - 1, 11, 1)
        slutt = dt.date(aar, 5, 31)

        antall_dager = (slutt - start).days + 1

        # Minst halvparten av dagene må ha målinger
        if len(maalinger) >= antall_dager / 2:

            skidager = 0

            for snodybde in maalinger.values():
                if snodybde >= 20:
                    skidager += 1

            resultat[aar] = skidager

    return resultat


# Lag grafen
plt.figure(figsize=(14, 7))

for stasjon, filnavn in filer.items():

    skidager = finn_skidager(filnavn)

    print(stasjon, "Antall skisesonger:", len(skidager))

    aarstall = sorted(skidager)
    antall = [skidager[aar] for aar in aarstall]

    if len(aarstall) > 0:
        plt.plot(
            aarstall,
            antall,
            marker="o",
            markersize=3,
            linewidth=1.5,
            label=stasjon
        )

plt.xlabel("Skisesong (sluttår)")
plt.ylabel("Antall dager med skiføre")
plt.title("Antall dager med skiføre per skisesong")

plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left")
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.show()


