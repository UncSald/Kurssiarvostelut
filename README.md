# Kurssiarvostelut
Tsoha harjoitustyö

Sovelluksen nimi on Kurssikarhu.

Kurssikarhu on sovellus, jossa käyttäjät voivat anonyymisti arvioida suorittamiaan kursseja.

Kurssikarhusta löytyy seuraavanlaiset toiminnot:

1. Kurssikarhuun voi luoda uniikin käyttäjätunnuksen.
    - Käyttäjätunnuksen olemassaolo tarkistetaan listasta ennen uuden tunnuksen luomista.
    - Salasana on syötettävä kahdesti.
    - Käyttäjätunnukseen ja salasanaan kelpuutettuja merkkejä on rajoitettu.

2. Käyttäjätunnuksella voi kirjautua sisään syöttämällä oikean salasanan.
    - Salasanat ovat tallennettuina listaan hajautusarvoina.

3. Kurssikarhun etusivulla on neljä listaa, joista ensimmäinen ilmoittaa viimeiseksi arvostellut 5 kurssia, toinen TOP 5 opettajat saamansa arvosanan mukaan, kolmas TOP 5 materiaalin ja neljäs TOP 5 vähiten työläät kurssit.

4. Kirjauduttuaan sisään käyttäjä voi arvioida kursseja erilliseltä sivulta löytyvällä lomakkeella.
    - Arvostelun kohteina ovat opettaja, materiaali ja vaaditun työn määrä.
    - Arvostelussa on myös avoin kenttä johon voi syöttää palautetta.
    - Arvostelulomakkeen tulokset tallentuvat taulukoihin.

5. Sisäänkirjautumisen jälkeen etusivulla on hakupalkki, josta voi hakea opettajaa nimellä tai kurssia tunnuksella.
    - Kurssisivulla kurssista on nähtävillä jokainen arvostelu.
    - Opettajasivulla on nähtävillä kurssit joilla opettaja on opettanut ja opettajan saamat arviot.
    - Opettajasta on myös tarjolla yhteiskeskiarvo kaikkien arvosteluiden mukaan.

6. Navigointipalkin kautta käyttäjä voi siirtyä haluamallensa sivulle:
    - Etusivulle, joka on auki kun sivu aukeaa.
    - Opettajat -sivulle, josssa opettajat ovat listattuina aakkosjärjestyksessä.
    - Kurssit -sivulle, jolta löytyvät kaikki tietokannan kurssit.
    - Kirjaudu sisään -sivulle
    - Luo käyttäjätunnus -sivulle
    - Käyttäjän kirjauduttua sisään palkki vaihtuu, ja tilalle ilmestyvät arviointilomake ja kirjaudu ulos painike.

7. Kurssi ja opettajasivuilla olevista listauksista pääsee tarkastelemaan kyseisten kurssien tai opettajien profiileita.
    - Profiilisivutoiminto on käytössä vasta sisäänkirjautumisen jälkeen.

Sovellus löytyy nyt myös fly.io :sta!
Sovelluksen saa käynnistettyä osoitteesta: https://kurssikarhu.fly.dev/

Ohjeet sovelluksen käynnistämiseen Flaskilla:
1. Kloonaa repositorio koneellesi haluamaasi sijaintiin komennolla ``` git clone https://github.com/UncSald/Kurssiarvostelut.git ```
2. Luo .env tiedosto ja määritä sen sisältö seuraavanlaiseksi:
    - DATABASE_URL = < tietokannan-paikallinen-osoite >
    - SECRET_KEY = < salainen-avain >
3. Aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet seuraavilla komennoilla:
    - ``` $ python3 -m venv venv ```
    - ``` $ source venv/bin/activate ```
    - ``` $ pip install -r ./requirements.txt ```
    - ``` $ psql < schema.sql ```
4. Käynnistä sovellus komennolla
    - ``` $ flask run ``` tai halutessasi ``` flask --app app.py --debug run ```
5. voit kirjautua sovellukseen tekemälläsi tunnuksella, tai valmiiksi olemassa olevalla admin tunnuksella
    - Tunnus: admin, Salasana: kurssikarhu