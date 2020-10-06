VCardEditor

VCardEditor on ohjelma, joka lukee, muokkaa, "siivoaa" ja tallentaa yhteystietoja
vcf.-tiedostomuodossa eli Vcard-formaatissa. (https://tools.ietf.org/html/rfc6350)
Tallennetut numerot voidaan siirtää takaisin puhelimeen, mikäli puhelin tätä
tukee. VCardEditor käy myös hyvin varmuuskopioiden tekemiseen ja ylläpitoon, sillä
duplikaatti-yhteystietoja ei voida samalla nimellä luoda tai tallentaa. On myös
mahdollista poistaa Suomen suuntanumerot yhteystiedoista, jolloin yhteystietojen käsittely
on yhdenmukaisempaa.

VCardEditor poistaa  Yhteystiedoista turhiksi katsomiaan komponentteja. Jäljelle
jäävät komponentit ovat nimi(koko nimi), puhelinnumerot ja sähköpostiosoitteet. Normaali peruskäyttäjä
tuskin tarvitsee muita ominaisuuksia. Tiedot nimen eri osista (etunimi, sukunimi tms.) myös sekoittavat
toimintaa kun käytetään useita eri alustoilla toimivia puhelimia, jotka soveltavat
Vcard-formaattia omilla tavoillaan. Näin VCardEditorin käyttö myös poistaa
etunimi-sukunimi -sähläämisen.


Komennot ja toiminta:

Control+N: Luo uuden yhteystiedon
Control+F: Aloittaa haun yhteystiedoista
Enter: Yhteystiedon ollessa valittuna avaa muokkausikkunan yhteystiedon muokkausta
    varten tai vaitoehtoisesti hakee yhteystiedoista
Control+E tai kaksoisklikkaus halutun yhteystiedon päällä: avaa yhteystiedon muokattavaksi
Control-O: Avaa tiedosto -ikkuna aukeaa, jolloin saa avattua vanhan yhteystietotiedoston muokkausta varen.
Control-s: Avaa tallenna nimellä -ikkunan. Muista lisätä halutun tiedostonimen perään
haluttu tiedostopääte eli .vcf.
delete: Yhteystiedon ollessa valittuna poistaa yhteystiedon
- tools-painikkeen takaa löytyy Remove Finish area code -toiminto
jolla saa poistettua joskus niin häiritsevät "+358" alut puhelnnumeroista.
- Haettaessa hakutoiminnolla hakee ohjelma nimien lisäksi myös puhelinnumeroista
ja sähköostiosoitteista

Toiminta yhteystiedon muokkaus -ikkunassa:

Control-S: Tallentaa syötetyt tiedot
Escape: Sulkee muokkausikkunan
Delete: Poistaa yhteystiedon
- Mikäli yrittää tallentaa tyhjää nimi- tai puhelinnumerokenttää, ohjelma poistaa
kyseiset tiedot.
- Esimerkkiyhteystietoja ei pysty tallentamaan.
