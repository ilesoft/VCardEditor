# -*- coding: utf-8 -*-
# TIE-02100-S2017 Johdatus ohjelmointiin
# Ilmari Marttila, ilmari.marttila@student.tut.fi
# opiskelijanumero:265040
# Tehtävän 13.11 ratkaisu.
# Taso: skaalautuva, koska numeroita ja meiliosoitteita voi lisätä
# mielivaltaisen määrän.
# Status: READY
# Ohjelman dokumentaatio ja kuvaus löytyy README.txt-tiedostosta tai
# käyttöliittymän Help-toiminnon takaa.

# Tämä tiedosto määrittelee yhteystietoluokan

class Contact:
    def __init__(self, name, tels=[], emails=[]):
        # tel on lista lisättävistä numeroista, email taas sposteista

        # Asetetaan oletusversio, johon yhteystiedot tullaan tallettamaan
        self.__version = '3.0'

        # formatted name
        self.__fn = name

        self.__tel = []
        for phone_number in tels:
            self.__tel.append(str(phone_number))

        self.__email = []
        for email in emails:
            self.__email.append(str(email))

        # Tallennetaan listaan nimen osat hakutoimintoja varten.
        self.search_string = name + ''.join(self.__tel) + ''.join(self.__email)

    def change_names(self, new_fn):
        """
        Metodi nimen muuttamiseen.
        :param new_fn: Asetettaa nimi
        :return: None
        """
        self.__fn = new_fn
        self.search_string = new_fn+''.join(self.__tel)+''.join(self.__email)

    def clear(self, tel=False, email=False, fn=False):
        """
        Ikkunoiden päivityksessä käytettävä metodi, joka
        mahdollistaa "ylikirjoituksen."
        :param tel:
        :param email:
        :return:
        """
        if tel:
            self.__tel.clear()
        if email:
            self.__email.clear()
        if fn:
            self.__fn = ''

    def get_info(self, type='search'):
        """
        :param type: on joko 'names'(default), 'tel','email' tai 'fn'
        riippuen siitä mistä halutaan tietoa.
        :return: Halutut tiedot. fn merkkijonona, muut listana.
        """
        # Ottaa parametrina type vaihtoehtoisesti 'tel' tai 'email'
        if type == 'search':
            return self.search_string
        elif type == 'tel':
            return self.__tel
        elif type == 'email':
            return self.__email
        elif type == 'fn':
            return self.__fn

    def add(self, param):
        """
        :param param: Puhelinnumero tai meiliosoite merkkijonona
        :return: False, jos oli duplikaatti, None jos ei lisättävää ja
        onnistuessa True.
        """
        if param == '':
            return
        try:
            # try-lohkoon toiminta joka suoritetaan mikäli kyseessä on numero.
            # Mikäli parametri on kirjaimia, siirrytään sitä
            # käsittelemään meilinä.
            int(param[1:])

            if param in self.__tel and not param == '+0000000000':
                return False

            if'+0000000000' in self.__tel:
                self.__tel.remove('+0000000000')
            if '' in self.__tel:
                self.__tel.remove('')

            self.__tel.append(param)
            return True

        except ValueError:
            if param in self.__email and not param == 'example@email.com':
                return False
            if 'example@email.com' in self.__email:
                self.__email.remove('example@email.com')
            if '' in self.__email:
                self.__email.remove('')

            self.__email.append(param)
            return True

    def remove_area_code(self):
        """
        Poistaa suomalaisen suuntanumeron yhteystiedon puhelinnumeroista
        ja tarkastaa duplikaatit pois.
        :return: None
        """
        old_list = self.__tel
        self.__tel = []
        index = 0
        for number in old_list:
            if number[:4] == '+358':
                if '0' + number[4:] not in self.__tel:
                    self.__tel.append('0' + number[4:])

            elif number not in self.__tel:
                self.__tel.append(number)

            index += 1
