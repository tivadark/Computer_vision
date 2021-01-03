#Kamondy Tivadar - 2020/21/1
#Computer vision course - Szechenyi Istvan University of Gyor
#Coin recognition application

import cv2
#OpenCv konyvtar importalasa

forint_ermek  = {
        "5 Ft": {
            "ertek": 5,
            "sugar": 37.5,
        },
        "10 Ft": {
            "ertek": 10,
            "sugar": 44.7,
        },
        "20 Ft": {
            "ertek": 20,
            "sugar": 51.2,
        },
        "50 Ft": {
            "ertek": 50,
            "sugar": 54.5,
        },
        "100 Ft": {
            "ertek": 100,
            "sugar": 40.7,
        },
        "200 Ft": {
            "ertek": 200,
            "sugar": 57.5,
        },
    }

def erme_detektalasa(ermek):
    kep = cv2.cvtColor(ermek, cv2.COLOR_BGR2GRAY) #a kep szurkearnyalatossa konvertalasa
    kep = cv2.medianBlur(kep, 21) #a kep elhomalyositasa a kep aprobb adatainak eltorlese vegett
    
    kor_alakzatok = cv2.HoughCircles(
        kep,  # bemeneti kep
        cv2.HOUGH_GRADIENT,  # detektalas tipusa
        1,
        50,
        param1=100,
        param2=50,
        minRadius=5,  # minimalis sugar meret
        maxRadius=350,  # max sugar
    )

    #kor_alakzatok detektalasa es a zold korvonal kirajzolasa korulottuk
    for felismert_kor_alakzatok in kor_alakzatok[0]: 
        x_koord, y_koord, detektalt_sugar = felismert_kor_alakzatok
        detektalt_ermek = cv2.circle( #a kor megrajzolasa a koordinatak es sugarak felhasznalasaval
            ermek,
            (int(x_koord), int(y_koord)),
            int(detektalt_sugar),
            (0, 255, 0),
            4,
        )

    return kor_alakzatok[0],detektalt_ermek

def osszeg_szamitas(ermek_adat,kuszobertek ,korvonalas_ermek):
    adat = {} #exportalando szotar
    for erme_adat in ermek_adat: #ermeken vegig iteralas
        for k in forint_ermek : #vegig iteralas az ermek eloredefinialt adatain
            if abs(erme_adat[2] - forint_ermek [k]["sugar"]) <= kuszobertek: #ha talalkozik a kuszobertekkel
                if k in adat.keys(): #ha a kulcs nem talalhato akkor hozzon letre egy ujat
                    adat[k] += 1
                else:
                    adat[k] = 1 #ermekhez hozzaadas
                cv2.putText(korvonalas_ermek, str(forint_ermek [k]["ertek"]), (int(erme_adat[0]), int(erme_adat[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 4) #az adott ermere az ertek kiiratasa
    return adat, korvonalas_ermek #adat es a kep visszaadasa mar az ertekekkel egyutt

if __name__ == "__main__":
    kep = cv2.imread('input_kepek/ermek1.jpg')

    ermek_adat,ermek_detektalt_kep = erme_detektalasa(kep) #ermek detektalasa
    cv2.imwrite("output_kepek/ermek_Hough.jpg",ermek_detektalt_kep)
    adat,kep = osszeg_szamitas(ermek_adat,1.5,ermek_detektalt_kep) #az ermek osszegenek szamitasa
    teljes_osszeg = 0
    
    for a in adat:
        print(a,": x", adat[a])
        teljes_osszeg += adat[a] * int(a.split(" ")[0])
    print("Teljes osszeg: ", teljes_osszeg)
    cv2.imwrite("output_kepek/ermek_darabertek_korvonal.jpg",kep)
