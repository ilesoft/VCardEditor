import quopri
from contact import Contact
from tkinter import filedialog


def filereader(path):
    vcf_file = open(path, "r", encoding="utf-8")
    # Siirretää listaan
    file_in_list = []
    for row in vcf_file:
        file_in_list.append(row)
    vcf_file.close()

    # Sanakirja, johon hyväksi havaitut yhteystiedot kirjataan
    # formaatissa {nimi:yhteystieto-olio,...}
    contacts_dict = {}

    # lippu, joka kertoo edellisen quoted_printable yhteystiedon jääneen kesken.
    onko_kesken = 0

    # kesken jäänyt nimi
    kesken = ""

    tel = ""
    for row in file_in_list:
        # Kaapataan uuden yhteystiedon alku.
        if "BEGIN:VCARD" in row or "begin:vcard" in row:
            telephone_numbers = []
            continue

        elif row[:2] == "FN" or row[:2] == "fn":
            fn_raw = row[2:]
            fn = fn_raw.split(":")
            fn = fn[len(fn) - 1]
            fn = fn.strip()
            # Mahdollistetaan QUOTED-PRINT-yhteensopivuus
            if "ENCODING=QUOTED-PRINTABLE" in fn_raw:
                if fn.endswith("="):
                    onko_kesken = 1
                    kesken = fn
                    continue
                fn = quopri.decodestring(fn)
                fn = fn.decode("utf-8")
            fn = fn.strip()
            continue

        elif row[:3] == "TEL":
            tel_raw = row[3:]
            tel = tel_raw.split(":")
            # Poimitaan riviltä numero
            tel = tel[len(tel) - 1]
            # Poistetaan mahdolliset välilyönnit numeroista.
            tel = tel.split()
            tel = "".join(tel)
            # Poistetaan mhdolliset ylimääräiset merkit numeroista.
            for character in ["-", "(", ")"]:
                tel = tel.split(character)
                tel = "".join(tel)
            # Poistetaan mahdollinen left-to-right embedding.
            tel = tel.strip("\u202a")
            tel = tel.strip("\u202c")

            tel = tel.strip()
            if tel not in telephone_numbers:
                telephone_numbers.append(tel)
            continue

        # Kaapataan yhteystiedon loppu ja tallennetaan se
        elif "END:VCARD" in row or "end:vcard" in row:
            # Tarkastellaan mahdolliset duplikaatit ja tallennetaan
            # tiedot sanakirjaan
            if fn not in contacts_dict:
                contacts_dict[fn] = Contact(fn, tels=telephone_numbers)

            else:
                if not tel == "":
                    contacts_dict[fn].add(tel)
            # Alustetaan muuttujat tyhjiksi, jottei mennä tiedoissa sekaisin.
            tel = ""
            fn = ""

        # otetaan huomioon kesken jääneet quoted_printaplet
        elif onko_kesken == 1:
            onko_kesken = 0
            row = row.strip()
            fn = quopri.decodestring(kesken + row[1:])
            fn = fn.decode("utf-8")
            fn = fn.strip()

    return contacts_dict


def filewriter(contact_files):
    new_vcf_file_path = filedialog.asksaveasfilename(
        title="Save As", filetypes=(("Vcard-file", "*.vcf"), ("text-file", "*.txt"))
    )
    new_vcf_file = open(new_vcf_file_path, "w", encoding="utf-8")
    for contact in sorted(contact_files, key=lambda name: name.upper()):
        print("BEGIN:VCARD\nVERSION:3.0", file=new_vcf_file)
        print("FN:", contact_files[contact].fn, sep="", file=new_vcf_file)
        for tel in contact_files[contact].tel:
            print("TEL;TYPE=VOICE;VALUE=text:", tel, sep="", file=new_vcf_file)

        print("END:VCARD", file=new_vcf_file)

    new_vcf_file.close()
