# a) PLotting og aggregering

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

with open("sinnes_2014_2025_med_makstemperatur.csv", encoding="utf-8-sig") as fil:
    leser = csv.reader(fil, delimiter=";")
    next(leser)
    
    for rad in leser:
        if len(rad) < 7 or rad[2].strip() == "":
            continue
        
        dato = datetime.strptime(rad[2].strip(), "%d.%m.%Y")

    temperatur = rad[3].strip().replace(",", ".")
    nedbør = rad[4].strip().replace(",", ".")
    vind = rad[5].strip().replace(",", ".")
    snødybde = rad[6].strip().replace(",", ".")

måneder = {}
