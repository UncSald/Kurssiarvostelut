# Kurssiarvostelut
Tsoha harjoitustyö

Sovelluksen nimi on Kurssikarhu.

Kurssikarhusta löytyy tällä hetkellä seuraavanlaiset toiminnot:

1. Kurssikarhuun voi luoda uniikin käyttäjätunnuksen.
- Käyttäjätunnuksen olemassaolo tarkistetaan listasta ennen uuden tunnuksen luomista.
- Virheilmoituksia en ole vielä luonut
2. Käyttäjätunnuksella voi kirjautua sisään syöttämällä oikean salasanan.
- Salasanat ovat tallennettuina listaan hajautusarvoina.
- Listaan on tulossa myös käyttäjäoikeuksiin liittyvä sarake
3. Kurssikarhun etusivulla on kaksi listaa, joista toinen ilmoittaa viimeiseksi arvostellut 5 kurssia ja toinen TOP 5 kurssit mateeriaalista saamansa arvosanan mukaan.
- Listauksissa seuraavaksi tavoitteena on luoda erillinen sivu jokaiselle kurssille.
- Kurssisivulla olisi tarkoituksena näkyä kurssin kokonais arvosana, opettajat ja jokainen arvostelu listattuna erikseen kuten esim. Google mapsissa. 

Ohjeet sovelluksen käynnistämiseen:
1. Kloonaa repositorio koneellesi haluamaasi sijaintiin komennolla "git clone https://github.com/UncSald/Kurssiarvostelut.git"
2. Luo .env tiedosto ja määritä sen sisältö seuraavanlaiseksi:
- DATABASE_URL = <tietokannan-paikallinen-osoite>
- SECRET_KEY = <salainen-avain>
3. Aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet seuraavilla komennoilla:
- $ python3 -m venv venv
- $ source venv/bin/activate
- $ pip install -r ./requirements.txt
- $ psql < schema.sql
4. Käynnistä sovellus komennolla
- $ flask run tai halutessasi flask --app app.py --debug run