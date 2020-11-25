#Kamondy Tivadar - 2020
#Computer vision course - Szechenyi Istvan University of Gyor
#erme recognition application

#TODO LIST:
#Ismeretlen meretu kor?
#Erme szin
#UI?

import cv2
import numpy as np

def erme_detektalasa():
    erme_forint = cv2.imread('input_kepek/ermek.jpg', 1)

    szurkeranyalatos = cv2.cvtColor(erme_forint, cv2.COLOR_BGR2GRAY)
    forraskep = cv2.medianBlur(szurkeranyalatos, 7)
    
    kor_alakzatok = cv2.HoughCircles( ##Hough kor transzformacio parameterezes
        forraskep,
        cv2.HOUGH_GRADIENT,  # detektalas tipusa
        1,
        50,
        param1=100,
        param2=50,
        minRadius=10,  # minimum sugar
        maxRadius=380,  # maximum sugar
    )

    ermek_masol = erme_forint.copy()

    for felismert_kor_alakzatok in kor_alakzatok[0]:
        x_koord, y_koord, detektalt_sugar = felismert_kor_alakzatok
        detektalt_ermek = cv2.circle(
            ermek_masol,
            (int(x_koord), int(y_koord)),
            int(detektalt_sugar),
            (0, 255, 0),
            4,
        )

    cv2.imwrite("output_kepek/ermek_Hough.jpg", detektalt_ermek)

    return kor_alakzatok

def osszeg_szamitas(): #TODO: szin hozzaadas
    ermek = {
        "5 Ft": {
            "ertek": 5,
            "sugar": 19.5,
            "arany": 1,
            "darab": 0,
        },
        "10 Ft": {
            "ertek": 10,
            "sugar": 21.5,
            "arany": 1.2,
            "darab": 0,
        },
        "20 Ft": {
            "ertek": 20,
            "sugar": 22.5,
            "arany": 1.249,
            "darab": 0,
        },
        "50 Ft": {
            "ertek": 50,
            "sugar": 25,
            "arany": 1.33,
            "darab": 0,
        },
        "100 Ft": {
            "ertek": 100,
            "sugar": 21,
            "arany": 1.115,
            "darab": 0,
        },
        "200 Ft": {
            "ertek": 200,
            "sugar": 30,
            "arany": 1.4,
            "darab": 0,
        },
    }

    kor_alakzatok = erme_detektalasa()
    sugar = []
    koordinatak = []

    for felismert_kor_alakzatok in kor_alakzatok[0]:
        x_koord, y_koord, detektalt_sugar = felismert_kor_alakzatok
        sugar.append(detektalt_sugar)
        koordinatak.append([x_koord, y_koord])

    legkisebb = min(sugar)
    kuszobertek = 0.0375
    teljes_osszeg = 0

    korvonalas_ermek = cv2.imread('output_kepek/ermek_Hough.jpg', 1)
    betutipus = cv2.FONT_HERSHEY_SIMPLEX

    for erme in kor_alakzatok[0]:
        arany_ell = erme[2] / legkisebb
        koord_x = erme[0]
        koord_y = erme[1]
        for forint in ermek:
            ertek = ermek[forint]['ertek']
            if abs(arany_ell - ermek[forint]['arany']) <= kuszobertek:
                ermek[forint]['darab'] += 1
                teljes_osszeg += ermek[forint]['ertek']
                cv2.putText(korvonalas_ermek, str(ertek), (int(koord_x), int(koord_y)), betutipus, 1,
                            (0, 0, 0), 4)

    print(f"Az ermek teljes osszege {teljes_osszeg} Ft")
    for forint in ermek:
        darabszam = ermek[forint]['darab']
        print(f"{darabszam}x = {forint}")


    cv2.imwrite("output_kepek/ermek_daraertek_korvonal.jpg", korvonalas_ermek)


if __name__ == "__main__": ##az osszeg kiszamolasa a __name__ guardot kovetoen
    osszeg_szamitas()
