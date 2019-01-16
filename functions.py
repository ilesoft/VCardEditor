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

# Tämä tiedosto sisältää funktiot, joita tarvitaan ohjelmassa Vcard-editor
# yhteystietojen lukemiseen vcf-tiedostosta ja kirjoittamiseen valittuun
# tiedostoon.

import quopri
from yhteystieto import Contact
from tkinter import filedialog


def filereader(path):

    vcf_file = open(path, 'r', encoding='utf-8')
    # Siirretää listaan
    file_in_list = []
    for row in vcf_file:
        file_in_list.append(row)
    vcf_file.close()

    # Sanakirja, johon hyväksi havaitut yhteystiedot kirjataan
    # formaatissa {...,nimi:yhteystieto-olio,...}
    contacts_dict = {}

    # lippu, joka kertoo edellisen quoted_printable yhteystiedon jääneen kesken.
    onko_kesken = 0

    # kesken jäänyt nimi
    kesken = ''

    email = ''
    tel = ''
    for row in file_in_list:
        # otetaan huomioon kesken jääneet quoted_printaplet
        if onko_kesken == 1 and row.startswith('='):
            onko_kesken = 0
            row = row.strip()
            fn = quopri.decodestring(kesken + row[1:])
            fn = fn.decode('utf-8')
            fn = fn.strip()

        # Kaapataan uuden yhteystiedon alku.
        elif 'BEGIN:VCARD' in row or 'begin:vcard' in row:
            new_contact = [[],[]]

        elif row[:2] == 'FN' or row[:2] == 'fn':
            fn_raw = row[2:]
            fn = fn_raw.split(':')
            fn = fn[len(fn)-1]
            fn = fn.strip()
            # Mahdollistetaan QUOTED-PRINT-yhteensopivuus
            if 'ENCODING=QUOTED-PRINTABLE' in fn_raw:
                if fn.endswith('='):
                    onko_kesken = 1
                    kesken = fn
                    continue
                fn = quopri.decodestring(fn)
                fn = fn.decode('utf-8')
            fn = fn.strip()

        elif row[:3] == 'TEL':
            tel_raw = row[3:]
            tel = tel_raw.split(':')
            # Poimitaan riviltä numero
            tel = tel[len(tel)-1]
            # Poistetaan mahdolliset välilyönnit numeroista.
            tel = tel.split()
            tel = ''.join(tel)
            # Poistetaan mhdolliset ylimääräiset merkit numeroista.
            for character in ['-', '(', ')']:
                tel = tel.split(character)
                tel = ''.join(tel)
            # Poistetaan mahdollinen left-to-right embedding.
            tel = tel.strip('\u202a')
            tel = tel.strip('\u202c')

            tel = tel.strip()
            if tel not in new_contact[0]:
                new_contact[0].append(tel)

        elif row[:5] == 'EMAIL':
            email_raw = row[5:]
            email = email_raw.split(':')
            email = email[len(email) - 1]
            email = email.strip()
            if email not in new_contact[1]:
                new_contact[1].append(email)

        # Kaapataan yhteystiedon loppu ja tallennetaan se
        elif 'END:VCARD' in row or 'end:vcard' in row:

            # Tarkastellaan mahdolliset duplikaatit ja tallennetaan
            #  tiedot sanakirjaan
            if fn not in contacts_dict:
                contacts_dict[fn] = Contact(fn, emails=new_contact[1],
                                            tels=new_contact[0])

            else:
                if  not tel=='':
                    contacts_dict[fn].add(tel)
                if not email=='':
                    contacts_dict[fn].add(email)
            # Alustetaan muuttujat tyhjiksi, jottei mennä tiedoissa sekaisin.
            tel = ''
            email = ''
            fn = ''


    return contacts_dict


def filewriter(contact_files):
    new_vcf_file_path = filedialog.asksaveasfilename(title='Save As',
                        filetypes=(("Vcard-file","*.vcf"),
                                   ("text-file","*.txt")))
    new_vcf_file = open(new_vcf_file_path, 'w', encoding='utf-8')
    for contact in sorted(contact_files, key=lambda name: name.upper()):
        print('BEGIN:VCARD\nVERSION:3.0',
                file=new_vcf_file)
        print('FN:', contact_files[contact].get_info(type='fn'),
                sep='',file=new_vcf_file)
        for tel in contact_files[contact].get_info(type='tel'):
            print('TEL;TYPE=VOICE;VALUE=text:', tel, sep='', file=new_vcf_file)
        for email in contact_files[contact].get_info(type='email'):
            print('EMAIL:', email, sep='', file=new_vcf_file)

        print('END:VCARD', file=new_vcf_file)

    new_vcf_file.close()
