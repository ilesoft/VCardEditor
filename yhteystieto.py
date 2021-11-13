# -*- coding: utf-8 -*-
# TIE-02100-S2017 Johdatus ohjelmointiin

class Contact:
    def __init__(self, name, tels=[]):
        # formatted name
        self.fn = name

        # tel on lista lisättävistä numeroista
        self.tel = []
        for phone_number in tels:
            self.tel.append(str(phone_number))

        # Tallennetaan listaan nimen osat hakutoimintoja varten.
        self.search_string = name + ''.join(self.tel)

    def change_names(self, new_fn):
        """
        Metodi nimen muuttamiseen.
        :param new_fn: Asetettaa nimi
        :return: None
        """
        self.fn = new_fn
        self.search_string = new_fn+''.join(self.tel)

    def clear(self, tel=False, fn=False):
        """
        Ikkunoiden päivityksessä käytettävä metodi, joka
        mahdollistaa "ylikirjoituksen."
        :param tel:
        :return:
        """
        if tel:
            self.tel.clear()
        if fn:
            self.fn = ''

    def add(self, param):
        """
        :param param: Puhelinnumero merkkijonona
        :return: False, jos oli duplikaatti, None jos ei lisättävää ja
        onnistuessa True.
        """
        if param == '':
            return
        try:
            # try-lohkoon toiminta, joka suoritetaan mikäli kyseessä on numero.
            int(param[1:])

            if param in self.tel:
                return False

            if '' in self.tel:
                self.tel.remove('')

            self.tel.append(param)
            return True

        except ValueError:
            False

    def remove_area_code(self):
        """
        Poistaa suomalaisen suuntanumeron yhteystiedon puhelinnumeroista
        ja tarkastaa duplikaatit pois.
        :return: None
        """
        old_list = self.tel
        self.tel = []
        index = 0
        for number in old_list:
            if number[:4] == '+358':
                if '0' + number[4:] not in self.tel:
                    self.tel.append('0' + number[4:])

            elif number not in self.tel:
                self.tel.append(number)

            index += 1
