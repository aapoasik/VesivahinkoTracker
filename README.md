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
  
1. Asenna Flask-kirjasto:
	$ pip install flask
2. Luo tietokantaan tarvittavat taulut:
	$ sqlite3 database.db < schema.sql
3. Käynnistä sovellus näin:
	$ flask run
