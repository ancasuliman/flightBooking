# Tema 2 SPRC - Flights booking system

Studenta: Suliman Anca    
Grupa: 342C1

## Descrierea implementarii

Pentru rezolvarea temei am creat 4 containere, pentru urmatoarele aplicatii:
* serverul mysql
* aplicatia server pentru sistemul de rezervari de bilete de avion
* aplicatia client
* aplicatia admin, care inregistreaza detaliile zborurilor in sistem

Interactiunea cu aplicatiile admin si client se realizeaza prin linia de comanda a containerelor aferente.   

Comenzile acceptate de aplicatia admin sunt:
* **adaugare_zbor**, dupa introducerea careia vor fi cerute informatiile necesare inregistrarii unui nou zbor in sistem (sursa, destinatie, ziua plecarii, ora plecarii, durata, numarul de locuri disponibile si un ID)

* **anulare_zbor**, dupa introducerea careia va fi solicitat ID-ul zborului care trebuie sters

Comenzile acceptate de aplicatia client sunt:
* **getOptimalRoute**, dupa introducerea careia vor fi cerute sursa, destinatia, numarul maxim de zboruri si ziua plecarii
aplicatia client va primi ca raspuns intreaga ruta care trebuie parcursa, astfel incat durata calatoriei de la sursa la destinatia precizate sa fie minima, cat si o lista cu ID-urile zborurilor care alcatuiesc ruta

* **bookTicket**, dupa introducerea careia vor fi cerute ID-urile zborurilor pentru ruta pentru care se doreste efectuarea rezervarii
aplicatia client va primi ca raspuns un ID de inregistrare a rezervarii in baza de date, sau un string vid in cazul in care rezervarea nu a putut fi efectuata pentru ruta mentionata

* **buyTicket**, dupa introducerea careia vor fi solicitate ID-ul rezervarii si detaliile cardului pentru efectuarea platii
aplicatia client va primi un boarding pass care include toate informatiile despre zborurile din ruta corespunzatoare rezervarii