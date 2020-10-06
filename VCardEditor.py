# -*- coding: utf-8 -*-
# TIE-02100-S2017 Johdatus ohjelmointiin

# Tämä tiedosto sisältää luokan, jolla käyttöliittymän luodaan

from functions import filereader, filewriter
from yhteystieto import Contact
from tkinter import filedialog, messagebox
from tkinter import *


class Vcard_GUI:
    def __init__(self):
        self.__main_window = Tk()
        self.__main_window.title('VCardEditor')
        self.__main_window.geometry('600x400')
        self.__main_window.minsize(100, 100)
        self.__main_window['bg'] = 'gray20'

        # Luodaan menuvalikko.
        menubar = Menu(self.__main_window)

        # Valikkorakenteet
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label='Open file', command=self.read_files)
        filemenu.add_command(label='New contact', command=self.new_contact)
        filemenu.add_command(label='Save as', command=self.save_as)
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=self.exit)
        menubar.add_cascade(label="File", menu=filemenu)

        toolmenu = Menu(menubar, tearoff=0)
        toolmenu.add_command(label='Remove Finnish area code',
                             command=self.remove_area_code)
        menubar.add_cascade(label='Tools', menu=toolmenu)
        self.__main_window.config(menu=menubar)

        menubar.add_command(label='Help', command=self.help)

        # Luodaan listaboxi, jossa näytetään yhteystietoja.
        self.__listbox = Listbox(self.__main_window, height=400, width=120,
                                 activestyle='none', bg='gray20',
                                 fg='gray70', selectbackground='yellow4',
                                 font=('Courier', 10))
        self.__scrollbar = Scrollbar(self.__main_window, orient=VERTICAL)
        self.__listbox['yscrollcommand'] = self.__scrollbar.set
        self.__scrollbar['command'] = self.__listbox.yview

        # Luodaan hakukenttä.
        self.__search_frame = Frame()
        self.__search_button = Button(self.__search_frame, text='Search',
                                      command=self.search)
        self.__search_entry = Entry(self.__search_frame)
        self.__clear_search_button = Button(self.__search_frame, text='X',
                                     command=self.clear_search)
        self.__how_many_label = Label(self.__search_frame, text=' 0 contacts ')

        self.__how_many_label.pack(side='right')
        self.__search_button.pack(side='right')
        self.__clear_search_button.pack(side='right')
        self.__search_entry.pack(side='left')

        # Sijoitetaan ikkunan sisältö
        self.__scrollbar.pack(side='right', fill=Y)
        self.__search_frame.pack(side='top')
        self.__listbox.pack(side='left', fill=BOTH, expand='1')

        # Lista sanakirjoista, johon yhteystiedot tallennetaan.
        self.__contact_files = {}

        # Bindings for editing contact.
        self.__listbox.bind('<Return>', self.edit_text)
        self.__listbox.bind('<Double-Button-1>', self.edit_text)
        self.__listbox.bind('<Control-e>', self.edit_text)

        # Binding for search
        self.__main_window.bind('<Control-f>',
                            lambda event:self.__search_entry.focus())
        self.__search_entry.bind('<Return>', self.search)

        # Binding for new contact.
        self.__main_window.bind('<Control-n>', self.new_contact)

        # Binding for deleting contact.
        self.__main_window.bind('<Delete>', lambda event: [self.edit_text(),
                                    self.delete(self.__contact_object),
                                    self.__edit_window.destroy(),
                                    self.update()])
        # Binding for openin files.
        self.__main_window.bind('<Control-o>', self.read_files)

        # Binding for save contacts.
        self.__main_window.bind('<Control-s>', self.save_as)

    def edit_text(self, event=None, new=False):
        # Mikäli mitää ei olla valittu muokattavaksi, ei avata muokkausikkunaa.
        if self.__listbox.curselection() == () and new == False:
            return

        self.__edit_window = Toplevel()
        self.__edit_window.title('Edit Contact')
        self.__edit_window.geometry('400x150')
        self.__edit_window.attributes('-topmost', 'true')
        self.__edit_window['bg'] = 'gray20'
        self.__edit_window.grab_set()
        if new:
            # Luotaessa uutta kontaktia, mennään tästä.
            self.__contact_object = Contact('Name')
            self.__contact_files['Name'] = self.__contact_object
            self.update()
        else:
            # Muokatessa vanhaa kontaktia, mennään tästä.
            name_and_others = self.__listbox.get(self.__listbox.curselection())
            name = name_and_others.split('|')[0].strip()
            self.__contact_object = self.__contact_files[name]

        name_label = Label(self.__edit_window, text='{:8>s}'.format('Name:'))
        name_label.grid(row=0, column=0, sticky=W + E)
        tel_label = Label(self.__edit_window, text='{:8>s}'.format('Phone:'))
        email_label = Label(self.__edit_window, text='{:8>s}'.format('Email:'))

        def save():
            """
            Tallentaa senhetkisen editointi-ikkunan tilanteen contact_files-
            listaan. Tarkastaa syötteiden oikeellisuuden.
            :return: None
            """
            # Täytyy tutkia onko samalla nimellä jo tietoja
            new_fn = name_entry.get()
            old_fn = self.__contact_object.get_info(type='fn')
            if new_fn == '':
                new_fn = 'Unnamed'
            if new_fn in self.__contact_files and new_fn != old_fn:
                yes = messagebox.askyesno('Name already exist',
                        'Previous data will vanish!\nDo you want to do that?')

                if yes:
                    del self.__contact_files[new_fn]
                    self.__contact_files[new_fn] = self.__contact_files.pop(old_fn)
                    self.__contact_object = self.__contact_files[new_fn]
                    self.__contact_object.change_names(new_fn)
                    self.update()

            elif new_fn != old_fn:
                self.__contact_files[new_fn] = self.__contact_files.pop(old_fn)
                self.__contact_object = self.__contact_files[new_fn]
                self.__contact_object.change_names(new_fn)

            # Tarkastetaan onko syötetty muita kuin numeroita.
            for tel in tel_entrys:
                if not tel.get()[1:].isdigit():
                    messagebox.showerror('Error', 'Number must be number!\nGet it?',
                                         parent=self.__edit_window)
                    return

            # Tarkastetaan mitä meilikenttään on syötetty.
            for email in email_entrys:
                if email.get().isdigit():
                    messagebox.showerror('Error', "Email can't be number!",
                                         parent=self.__edit_window)
                    return

            self.__contact_object.clear(tel=True, email=True)

            # Poistetaan turhat tel-entry-kentät
            removable = []
            index = 0
            for tel in tel_entrys:
                number = tel.get()
                if not number[1:].isdigit():
                    messagebox.showerror('Error', 'It meant phone NUMBER!')
                    return
                if number == '+0000000000' or number == '':
                    tel.grid_remove()
                    removable.append(index)
                    number = ''

                if number != '':
                    int(number[1:])
                    self.__contact_object.add(number)
                    index += 1

            if len(removable) != 0:
                for removable_num in removable:
                    del tel_entrys[removable_num]

            # Poistetaan turhat email-entry-kentät
            removable = []
            index = 0
            for email in email_entrys:
                adress = email.get()
                if adress == 'example@email.com' or adress == '':
                    email.grid_remove()
                    removable.append(index)
                    adress = ''
                self.__contact_object.add(adress)
                index += 1
            if len(removable) != 0:
                for removable_email in removable:
                    del email_entrys[removable_email]

            update_edit_window()
            # Päivitetään listboxi
            self.update()

        def want_to_save(event=None):
            """
            Kun editointi-ikkunaa yritetään sulkea raksista tai painamalla
            Escape-näppäintä, kysytään, haluaako käyttäjä tallentaa.
            :return:
            """
            want_save = messagebox.askyesno('Oops', 'Want to save?',
                                            parent=self.__edit_window)
            if want_save:
                ok_button.invoke()
            else:
                self.__edit_window.destroy()

        save_button = Button(self.__edit_window, text='Save', command=save)
        self.__edit_window.bind('<Control-s>', lambda event: save_button.invoke())
        ok_button = Button(self.__edit_window, text='OK',
                           command=lambda: [save(), self.__edit_window.destroy()])
        self.__edit_window.bind('<Escape>', want_to_save)
        self.__edit_window.protocol("WM_DELETE_WINDOW", want_to_save)

        delete_button = Button(self.__edit_window, text='Delete',
                               command=lambda: [save, self.delete(self.__contact_object),
                                                self.__edit_window.destroy(),
                                                self.update()])
        self.__edit_window.bind('<Delete>', lambda event: delete_button.invoke())

        # Luodaan Entry-kenttä nimelle.
        name_entry = Entry(self.__edit_window)

        # Luodaan Entry-kentät puhelinnumeroille.
        tels = self.__contact_object.get_info(type='tel')
        tel_entrys = []
        for i in range(len(tels)):
            tel_entrys.append(Entry(self.__edit_window))

        # Luodaan Entry-kentätä meileille.
        emails = self.__contact_object.get_info(type='email')
        email_entrys = []
        for i in range(len(emails)):
            email_entrys.append(Entry(self.__edit_window))

        def add_tel_entry():
            # Lisätään uusi yhteystietokenttä, jos se on järkevää
            save()
            if '+0000000000' not in self.__contact_object.get_info(type='tel'):
                self.__contact_object.add('+0000000000')
                tel_entrys.append(Entry(self.__edit_window))
            update_edit_window()

        def add_email_entry():
            # Lisätään uusi yhteystietokenttä, jos se on järkevää
            save()
            if 'example@email.com' not in \
                    self.__contact_object.get_info(type='email'):
                self.__contact_object.add('example@email.com')
                email_entrys.append(Entry(self.__edit_window))
            update_edit_window()

        add_telb = Button(self.__edit_window, text='+', command=add_tel_entry)
        add_emailb = Button(self.__edit_window, text='+',
                            command=add_email_entry)

        def update_edit_window():
            # Päivitetään editointi-ikkuna
            tel_label.grid(row=1, column=0, sticky=W + E)
            email_label.grid(row=2, column=0, sticky=W + E)
            save_button.grid(row=3, column=2)
            ok_button.grid(row=3, column=3)
            delete_button.grid(row=3, column=1)

            name_entry.delete(0, 'end')
            name_entry.insert(0, self.__contact_object.get_info(type='fn'))
            name_entry.grid(row=0, column=1, sticky=W + E)

            # Päivitetään puhelinnumerot.
            i = 0
            for tel in tel_entrys:
                tel.delete(0, 'end')
                tel.insert(0, self.__contact_object.get_info(type='tel')[i])
                tel.grid(row=1, column=1 + i, sticky=W + E)
                i += 1
            add_telb.grid(row=1, column=1 + i, sticky=W)

            # Päivitetään meilit.
            i = 0
            for email in email_entrys:
                email.delete(0, 'end')
                email.insert(0, self.__contact_object.get_info(type='email')[i])
                email.grid(row=2, column=1 + i, sticky=W + E)
                i += 1
            add_emailb.grid(row=2, column=1+i, sticky=W)

        update_edit_window()

        # Avattaessa edit_ikkunaa asetetaan kursori valmiiksi sopivaan paikkaan
        self.__edit_window.focus()
        if new:
            name_entry.focus()
        else:
            try:
                tel_entrys[0].focus()
            except IndexError:
                pass

    def read_files(self, event=None):
        # Selvitetään avattava tiedosto ja lisätään tiedostosta yhteystietoja
        file_path = filedialog.askopenfilename(
            initialdir="\\", title="Open file",
            filetypes=(("Vcard files", "*.vcf"),
                       ("all files", "*.*")))

        if file_path == '':
            pass
        else:
            # Palauttaa sanakirjan yhteystieto-olioista
            files_read = filereader(file_path)

            # Lisätään uudet yhteystiedot sanakirjaan mikäli eivät siellä vielä ole
            # yt = yhteystieto
            for yt in files_read:
                if yt in self.__contact_files:

                    for number in files_read[yt].get_info(type='tel'):
                        self.__contact_files[yt].add(number)

                    for email in files_read[yt].get_info(type='email'):
                        self.__contact_files[yt].add(email)
                else:
                    self.__contact_files[yt] = files_read[yt]

            # Päivitetään myöskin pääikkuan listboxi, jotta se pysyy ajan
            # tasalla
            self.update()
            self.__listbox.selection_set(0)
            self.__listbox.focus_set()

    def save_as(self, event=None):
        # Tallentaa muokattavat yhteystiedot valittuun tiedotoon.
        filewriter(self.__contact_files)

    def new_contact(self, event=None):
        # Luo uuden yhteystiedon, jota ruvetaan heti muokkaamaan.
        self.edit_text(new=True)

    def search(self, event=None):
        """
        Metodi kerää omaan sanakirjaansa ne yhteystieto-oliot, jotka sopivat
        annettuun hakusanaan, ja kutsuu sen jälkeen uptade-metodia, joka
        päivittää listboxiin hakutulokset.
        :return:
        """
        search_result = {}
        search_word = self.__search_entry.get()
        # Otetaan huomioon se, että painetaan enteriä hakukentän ollessa tyhjä.
        if search_word == '':
            self.update()
            return

        # Käydään läpi kaikki yhteystiedot ja etsitään hakusanaa.
        for contact in self.__contact_files:
            search_string = self.__contact_files[contact].get_info(type='search')
            if search_word in search_string or\
                    search_word.capitalize() in search_string or\
                    search_word.upper() in search_string or\
                    search_word.lower() in search_string:
                search_result[contact] = self.__contact_files[contact]

        self.update(search=True, search_dict=search_result)
        # Aktivoidaan ensimmäinen haktulos valmiiksi käytön nopeuttamiseksi.
        self.__listbox.selection_set(0)
        self.__listbox.focus_set()

    def clear_search(self):
        # Tyhjentää hakukentän ja päivittää ruudulle kaikki yhteystiedot.
        self.update()
        self.__search_entry.delete(0, END)

    def start(self):
        self.__main_window.mainloop()

    def exit(self):
        self.__main_window.destroy()

    def update(self, search=False, search_dict=None):
        """

        :param search: Ollaanko esittämässä hakutuloksia vai kaikkia kontakteja
        :param search_dict: Mahdollinen lista hakutuloksista,
        jotko voidan esittää käyttäjälle.
        :return: None
        """
        # Otetaan talteen sen hetkinen valinta:
        try:
            selection = int(self.__listbox.curselection()[0])
        except:
            pass

        # Tyhjennetään listboxi päivitystä varten.
        self.__listbox.delete(0, END)

        if search:
            for_listbox = search_dict
        else:
            for_listbox = self.__contact_files

        index = 0
        for name in sorted(for_listbox, key=lambda name: name.upper()):
            number = self.__contact_files[name].get_info(type='tel')
            email = self.__contact_files[name].get_info(type='email')

            # jos tietyt tietueet ovat tyhjiä niiden paikalle näytetään tyhjää.
            if email == []:
                email = ['']
            if number == []:
                number = ['']

            shown = '{:30s}|{:30s}|{:}'.format(name, ' | '.join(number),
                                            ' | '.join(email))
            self.__listbox.insert(index, shown)
            index += 1

        # Koitetaan valita sama listboxin alkio, tai ainakin seuraava, tai
        # ainakin edellinen.
        try:
            self.__listbox.selection_set(selection)
            self.__listbox.see(selection)
        except:
            try:
                self.__listbox.selection_set(selection - 1)
                self.__listbox.see(selection - 1)
            except:
                pass

        # Koitetaan saada entinen valinta näkyviin.
        try:
            self.__listbox.see(selection)
        except:
            pass

        # Kerrotaan käyttäjälle, montako yhteystietoa on käsittelyssä
        self.__how_many_label['text'] = '{:} contacts'.format(len(for_listbox))

    def delete(self, object):
        """
        Poistaa valitun yhteystiedon contact_files sanakirjasta ja koko ohjelmasta.
        :param object: Poistettava yhteystieto.
        :return: None
        """
        key_to_remove = object.get_info(type='fn')
        if messagebox.askyesno('Deleting contact', 'Do you want to delete '
                                                      + 'this contact?',
                               parent=self.__edit_window):
            del self.__contact_files[key_to_remove]
            self.update()
        else:
            return

    def remove_area_code(self):
        """
        Poistaa suomen suuntanumern kaikista yhteystiedoista.
        :return: None
        """
        for contact in self.__contact_files:
            self.__contact_files[contact].remove_area_code()
        self.update()

    def help(self):
        """
        Avaa ohjeikkunan, jossa kerrotaan ohjelmasta.
        :return:
        """
        help_window = Toplevel()
        help_window.title('Help')
        help_window.geometry('600x700')
        help_window.attributes('-topmost', 'true')
        help_window['bg'] = 'gray20'

        # Infotekstit
        try:
            info_file = open('README.md', 'r', encoding='utf-8')
            info_text = ''
            for row in info_file:
                info_text += row
            info_file.close()
        except:
            info_text = 'Error while reading README-file. It can be moved\n'\
                                    + 'or removed from the programs folder'
        infolabel = Label(help_window, text=info_text,
                                 bg='gray20', fg='gray70', justify=LEFT,
                          font=('Helvetica', 8))
        infolabel.pack(side='top')
        ok_button = Button(help_window, text='OK', command=help_window.destroy)
        ok_button.pack(side='bottom')


def main():
    ikkuna = Vcard_GUI()
    ikkuna.start()


main()
