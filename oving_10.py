# OPPGAVE A)

# Importere bibliotekene
import csv
import matplotlib.pyplot as plt
from datetime import datetime

# Oversikt over værstasjonene og kobler dem til CSV-filene
værstasjoner = {
    "Sinnes": {
        "fil": "sinnes_2014_2025_med_makstemperatur.csv",
        "kolonner": [3, 4, 5, 6]
    },
    "Oslo Blindern": {
        "fil": "oslo_blindern_1954_2025_med_makstemperatur.csv",
        "kolonner": [4, 5, 6, 7]
    },
    "Røros": {
        "fil": "roeros_1954_2025_med_makstemperatur.csv",
        "kolonner": [4, 5, 6, 7]
    },
    "Tromsø": {
        "fil": "tromsoe_1954_2025_med_makstemperatur.csv",
        "kolonner": [4, 5, 6, 7]
    },
    "Værnes": {
        "fil": "vaernes_1954_2025_med_makstemperatur.csv",
        "kolonner": [4, 5, 6, 7]
    },
    "Venabu": {
        "fil": "venabu_1954_2025_med_makstemperatur.csv",
        "kolonner": [4, 5, 6, 7]
    }
}

# Lager en tom dictionary til å samle værdataene
resultater = {}

# Leser inn data som står i filene, går gjennom alle værstasjonene
for stasjon in værstasjoner:

    filnavn = værstasjoner[stasjon]["fil"]
    kolonner = værstasjoner[stasjon]["kolonner"]

    temperatur_kolonne = kolonner[0]
    nedbør_kolonne = kolonner[1]
    vind_kolonne = kolonner[2]
    snø_kolonne = kolonner[3]

    måneder = {}

    with open(filnavn, encoding="utf-8-sig") as fil:
        leser = csv.reader(fil, delimiter=";")
        next(leser)

# Går gjennom hver enkel rad i CSV-filen, samler målingene fra samme måned og år
        for rad in leser:

            if len(rad) <= snø_kolonne or rad[2].strip() == "":
                continue

            dato = datetime.strptime(rad[2].strip(), "%d.%m.%Y")
            måned = dato.strftime("%Y-%m")

# Samler målingene i riktig måned
            if måned not in måneder:
                måneder[måned] = {
                    "temperatur": [],
                    "nedbør": [],
                    "vind": [],
                    "snødybde": []
                }

# Gjør komma til punktum i desimaltall (brukt av Python)
            temperatur = rad[temperatur_kolonne].strip().replace(",", ".")
            nedbør = rad[nedbør_kolonne].strip().replace(",", ".")
            vind = rad[vind_kolonne].strip().replace(",", ".")
            snødybde = rad[snø_kolonne].strip().replace(",", ".")

# Gjør at tom tekst eller en bindestrek ikke regnes som gyldige målinger
# Lager til nye målinger som ikke er registrert enda
            if temperatur != "" and temperatur != "-":
                måneder[måned]["temperatur"].append(float(temperatur))

            if nedbør != "" and nedbør != "-":
                måneder[måned]["nedbør"].append(float(nedbør))

            if vind != "" and vind != "-":
                måneder[måned]["vind"].append(float(vind))

            if snødybde != "" and snødybde != "-":
                måneder[måned]["snødybde"].append(float(snødybde))

    resultater[stasjon] = måneder


# Beregner månedsverdiene, verdiene oppgaven spør etter
# Går gjennom hver værstasjon og hver måned
# Ferdigstiller listene
månedlige_resultater = {}

for stasjon in resultater:

    måneder = resultater[stasjon]

    månedlige_resultater[stasjon] = {
        "datoer": [],
        "maks_snø": [],
        "total_nedbør": [],
        "maks_temp": [],
        "min_temp": [],
        "maks_vind": []
    }

    for måned in sorted(måneder):

        temperatur = måneder[måned]["temperatur"]
        nedbør = måneder[måned]["nedbør"]
        vind = måneder[måned]["vind"]
        snødybde = måneder[måned]["snødybde"]

        resultat = månedlige_resultater[stasjon]

        resultat["datoer"].append(
            datetime.strptime(måned, "%Y-%m")
        )

# Teller hvor mange gyldige snømålinger
# Finner største snødybde
# Resultatet None hvis listen er tom
        if len(snødybde) > 0:
            resultat["maks_snø"].append(max(snødybde))
        else:
            resultat["maks_snø"].append(None)

# Nedbør krever mer enn 20 gyldige målinger
# Hvis det er mer enn 20, legges alle målingene sammen
# Hvis det er mindre, registreres ikke totalsummen
        if len(nedbør) > 20:
            resultat["total_nedbør"].append(sum(nedbør))
        else:
            resultat["total_nedbør"].append(None)
            print(stasjon, måned,
                  "- Ikke registrert total nedbør denne måneden")

# Finner den høyeste og laveste temperaturen
        if len(temperatur) > 0:
            resultat["maks_temp"].append(max(temperatur))
            resultat["min_temp"].append(min(temperatur))
        else:
            resultat["maks_temp"].append(None)
            resultat["min_temp"].append(None)

# Finner den høyeste registrerte middelvinden i måneden
        if len(vind) > 0:
            resultat["maks_vind"].append(max(vind))
        else:
            resultat["maks_vind"].append(None)


# Lager grafer med matplotlib
# Plotting av resultatene
plt.figure(figsize=(12, 12))

# Graf 1: Maksimal snødybde
plt.subplot(4, 1, 1)

for stasjon in månedlige_resultater:
    data = månedlige_resultater[stasjon]

    plt.plot(data["datoer"], data["maks_snø"], label=stasjon)

plt.title("Maksimal snødybde per måned")
plt.ylabel("Snødybde (cm)")
plt.legend()
plt.grid()


# Graf 2: Total nedbør
plt.subplot(4, 1, 2)

for stasjon in månedlige_resultater:
    data = månedlige_resultater[stasjon]

    plt.plot(data["datoer"], data["total_nedbør"], label=stasjon)

plt.title("Total nedbør per måned")
plt.ylabel("Nedbør (mm)")
plt.legend()
plt.grid()


# Graf 3: Maksimum og minimum middeltemperatur
plt.subplot(4, 1, 3)

for stasjon in månedlige_resultater:
    data = månedlige_resultater[stasjon]

    plt.plot(data["datoer"], data["maks_temp"],
             label=stasjon + " maks")

    plt.plot(data["datoer"], data["min_temp"],
             label=stasjon + " min")

plt.title("Maksimum og minimum middeltemperatur per måned")
plt.ylabel("Temperatur (°C)")
plt.legend()
plt.grid()


# Graf 4: Maksimal middelvind
plt.subplot(4, 1, 4)

for stasjon in månedlige_resultater:
    data = månedlige_resultater[stasjon]

    plt.plot(data["datoer"], data["maks_vind"], label=stasjon)

plt.title("Maksimal middelvind per måned")
plt.xlabel("Dato")
plt.ylabel("Vind (m/s)")
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()

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

# OPPGAVE D)

from statistics import median

# Lager tomme lister for alle månedene
vind_per_måned = {}

for måned in range(1, 13):
    vind_per_måned[måned] = []

# Samler vindmålingene fra alle år
# Bruker Sinnes som værstasjon
for måned in resultater["Sinnes"]:

    månedsnummer = datetime.strptime(måned, "%Y-%m").month

    vind = resultater["Sinnes"][måned]["vind"]

# Legger alle målingene inn i listen for den aktuelle måneden
    vind_per_måned[månedsnummer].extend(vind)


# Beregner minimum, median og maksimum
# Lager tre lister, går gjennom alle månedene
min_vind = []
median_vind = []
maks_vind = []

for måned in range(1, 13):

    vind = vind_per_måned[måned]

# Bruker None dersom en måned ikke har noen gyldige målinger
    if len(vind) > 0:

        min_vind.append(min(vind))
        median_vind.append(median(vind))
        maks_vind.append(max(vind))

    else:
        min_vind.append(None)
        median_vind.append(None)
        maks_vind.append(None)


# Plotting
månedsnavn = [
    "Januar", "Februar", "Mars", "April",
    "Mai", "Juni", "Juli", "August",
    "September", "Oktober", "November", "Desember"
]

plt.figure(figsize=(12, 6))

plt.plot(månedsnavn, min_vind, label="Minimum")
plt.plot(månedsnavn, median_vind, label="Median")
plt.plot(månedsnavn, maks_vind, label="Maksimum")

plt.title("Minimum, median og maksimum vindstyrke på Sinnes")
plt.xlabel("Måned")
plt.ylabel("Vindstyrke (m/s)")
plt.legend()
plt.grid()

plt.tight_layout()
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
