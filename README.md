# VesivahinkoTracker
Web-sovellus Kumpulan kampuksen tilojen vesivahinkojen raportointiin
  
Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.  
Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan raportteja.  
Käyttäjä näkee sovellukseen lisätyt raportit.  
Käyttäjä pystyy etsimään raportteja sijainnin perusteella.  
Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja käyttäjän lisäämät raportit.  
Käyttäjä pystyy valitsemaan raportille luokittelun (sijainti).  
Käyttäjä pystyy reagoimaan raportteihin asiaankuuluvilla emojeilla.  
  
Sovelluksen käyttöönotto:  
  
Asenna Flask-kirjasto:
   ~~~ 
	$ pip install flask
   ~~~
Luo tietokanta ja alusta siihen tarvittavat taulut:
   ~~~ 
  $ sqlite3 database.db < schema.sql
   ~~~ 
Käynnistä sovellus näin:
   ~~~ 
  $ flask run
   ~~~


# Testaus suurella tietomäärällä

Sovellusta testattiin suurella tietomäärällä seed.py-tiedoston avulla. Seed.py-tiedosto tyhjentää tietokannan, jonka jälkeen se populoi 100 000 käyttäjää, 1 000 000 raporttia ja hajautettua reaktiota, sekä 100 000 reaktiota, jotka kohdistetaan yhteen raporttiin.

Tietyt toiminnot toimivat voivat toimia normaalia hitaammin (esim. käyttäjäsivut ja haku), sillä niillä voi esiintyä normaalia enemmän dataa, eikä niillä ole sivutusta. Jos esimerkiksi haetaan 'u', haku palauttaa kaikki tietokannassa olevat raportit (sillä jokaisen on tehnyt käyttäjä *u*serXXXX), mikä vie noin 15 sekuntia. Tämä ei kuitenkaan ole realistinen ongelma tavallisessa käytössä: esimerkiksi jos haetaan jotain tiettyä kohdetta, haku toimii edelleen riittävän nopeasti, ja käyttäjäsivutkin toimivat riittävän hyvin. Muut sovelluksen toiminnot toimivat edelleen erinomaisesti.
