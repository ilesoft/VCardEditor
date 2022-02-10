# VCardEditor

VCardEditor on ohjelma, joka lukee, muokkaa, "siivoaa" ja tallentaa yhteystietoja vcf-tiedostomuodossa eli Vcard-formaatissa. [RFC6350](https://tools.ietf.org/html/rfc6350) Tallennetut numerot voidaan siirtää takaisin puhelimeen, mikäli puhelin tätä tukee. VCardEditor käy myös hyvin varmuuskopioiden tekemiseen ja ylläpitoon, sillä duplikaatti-yhteystietoja ei voida samalla nimellä luoda tai tallentaa. On myös mahdollista poistaa Suomen suuntanumerot yhteystiedoista, jolloin yhteystietojen käsittely on yhdenmukaisempaa.

VCardEditor poistaa  Yhteystiedoista turhiksi katsomiaan komponentteja. Jäljelle jäävät komponentit ovat nimi (koko nimi) ja puhelinnumero. Normaali peruskäyttäjä tuskin tarvitsee muita ominaisuuksia. Tiedot nimen eri osista (etunimi, sukunimi tms.) myös sekoittavat toimintaa kun käytetään useita eri alustoilla toimivia puhelimia, jotka soveltavat Vcard-formaattia omilla tavoillaan. Näin VCardEditorin käyttö myös poistaa etunimi-sukunimi -sähläämisen.

## Komennot ja toiminta:

- ctrl-N: Luo uuden yhteystiedon
- ctrl-F: Aloittaa haun yhteystiedoista
- Enter: Yhteystiedon ollessa valittuna avaa muokkausikkunan yhteystiedon muokkausta varten tai vaitoehtoisesti hakee yhteystiedoista
- ctrl-E tai kaksoisklikkaus halutun yhteystiedon päällä: avaa yhteystiedon muokattavaksi
- ctrl-O: Avaa tiedosto -ikkuna aukeaa, jolloin saa avattua vanhan yhteystietotiedoston muokkausta varen.
- ctrl-s: Avaa tallenna nimellä -ikkunan. Muista lisätä halutun tiedostonimen perään haluttu tiedostopääte eli .vcf.
- delete: Yhteystiedon ollessa valittuna poistaa yhteystiedon

tools-painikkeen takaa löytyy Remove Finish area code -toiminto jolla saa poistettua joskus niin häiritsevät "+358" alut puhelnnumeroista.

## Toiminta yhteystiedon muokkaus -ikkunassa

- ctrl-S: Tallentaa syötetyt tiedot
- Esc: Sulkee muokkausikkunan
- Delete: Poistaa yhteystiedon
