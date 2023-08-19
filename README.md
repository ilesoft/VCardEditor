# VCardEditor

VCardEditor on ohjelma, joka lukee, muokkaa, "siivoaa" ja tallentaa yhteystietoja vcf-tiedostomuodossa eli Vcard-formaatissa. [RFC6350](https://tools.ietf.org/html/rfc6350) Tallennetut numerot voidaan siirtää takaisin puhelimeen, mikäli puhelin tätä tukee. VCardEditor käy myös hyvin varmuuskopioiden tekemiseen ja ylläpitoon, sillä duplikaatti-yhteystietoja ei voida samalla nimellä luoda tai tallentaa. On myös mahdollista poistaa Suomen suuntanumerot yhteystiedoista, jolloin yhteystietojen käsittely on yhdenmukaisempaa.

VCardEditor poistaa  Yhteystiedoista turhiksi katsomiaan komponentteja. Jäljelle jäävät komponentit ovat nimi (koko nimi) ja puhelinnumero. Normaali peruskäyttäjä tuskin tarvitsee muita ominaisuuksia. Tiedot nimen eri osista (etunimi, sukunimi tms.) myös sekoittavat toimintaa kun käytetään useita eri alustoilla toimivia puhelimia, jotka soveltavat Vcard-formaattia omilla tavoillaan.

_Remove Finish area code_ -toiminlla saa poistettua "+358" alut puhelinnumeroista.
