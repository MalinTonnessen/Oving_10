# OPPGAVE A)

import csv
import matplotlib.pyplot as plt
from datetime import datetime

# Oversikt over værstasjonene og CSV-filene
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

resultater = {}

# Leser inn data fra alle værstasjonene
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

        for rad in leser:

            if len(rad) <= snø_kolonne or rad[2].strip() == "":
                continue

            dato = datetime.strptime(rad[2].strip(), "%d.%m.%Y")
            måned = dato.strftime("%Y-%m")

            if måned not in måneder:
                måneder[måned] = {
                    "temperatur": [],
                    "nedbør": [],
                    "vind": [],
                    "snødybde": []
                }

            temperatur = rad[temperatur_kolonne].strip().replace(",", ".")
            nedbør = rad[nedbør_kolonne].strip().replace(",", ".")
            vind = rad[vind_kolonne].strip().replace(",", ".")
            snødybde = rad[snø_kolonne].strip().replace(",", ".")

            if temperatur != "" and temperatur != "-":
                måneder[måned]["temperatur"].append(float(temperatur))

            if nedbør != "" and nedbør != "-":
                måneder[måned]["nedbør"].append(float(nedbør))

            if vind != "" and vind != "-":
                måneder[måned]["vind"].append(float(vind))

            if snødybde != "" and snødybde != "-":
                måneder[måned]["snødybde"].append(float(snødybde))

    resultater[stasjon] = måneder


# Beregner månedsverdiene
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

        if len(snødybde) > 0:
            resultat["maks_snø"].append(max(snødybde))
        else:
            resultat["maks_snø"].append(None)

        if len(nedbør) > 20:
            resultat["total_nedbør"].append(sum(nedbør))
        else:
            resultat["total_nedbør"].append(None)
            print(stasjon, måned,
                  "- Ikke registrert total nedbør denne måneden")

        if len(temperatur) > 0:
            resultat["maks_temp"].append(max(temperatur))
            resultat["min_temp"].append(min(temperatur))
        else:
            resultat["maks_temp"].append(None)
            resultat["min_temp"].append(None)

        if len(vind) > 0:
            resultat["maks_vind"].append(max(vind))
        else:
            resultat["maks_vind"].append(None)


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


# OPPGAVE D)

from statistics import median

# Samler vindmålingene fra alle år
vind_per_måned = {}

for måned in range(1, 13):
    vind_per_måned[måned] = []

# Bruker Sinnes som værstasjon
for måned in resultater["Sinnes"]:

    månedsnummer = datetime.strptime(måned, "%Y-%m").month

    vind = resultater["Sinnes"][måned]["vind"]

    vind_per_måned[månedsnummer].extend(vind)


# Beregner minimum, median og maksimum
min_vind = []
median_vind = []
maks_vind = []

for måned in range(1, 13):

    vind = vind_per_måned[måned]

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
