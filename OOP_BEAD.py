import tkinter as tk
from tkinter import messagebox, simpledialog, Menu, Label, Button
from datetime import datetime
from abc import ABC, abstractmethod

class Szoba(ABC):
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar

    @abstractmethod
    def leiras(self):
        pass

class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam, ar):
        super().__init__(szobaszam, ar)

    def leiras(self):
        return f"Egyágyas szoba, szobaszám: {self.szobaszam}, ár: {self.ar} Ft"

class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam, ar):
        super().__init__(szobaszam, ar)

    def leiras(self):
        return f"Kétágyas szoba, szobaszám: {self.szobaszam}, ár: {self.ar} Ft"

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []

    def szoba_hozzaad(self, szoba):
        self.szobak.append(szoba)

class Foglalas:
    def __init__(self):
        self.foglalasok = []

    def foglal(self, szalloda, szobaszam, datum):
        for szoba in szalloda.szobak:
            if szoba.szobaszam == szobaszam:
                if any(f['datum'] == datum and f['szobaszam'] == szobaszam for f in self.foglalasok):
                    return "Ez a szoba már foglalt ezen a napon."
                else:
                    self.foglalasok.append({'szobaszam': szobaszam, 'datum': datum, 'ar': szoba.ar})
                    return f"Foglalás rögzítve: {szobaszam}, dátum: {datum}, ár: {szoba.ar} Ft"
        return "Nincs ilyen szobaszám."

    def lemond(self, szobaszam, datum):
        for i, foglalas in enumerate(self.foglalasok):
            if foglalas['szobaszam'] == szobaszam and foglalas['datum'] == datum:
                del self.foglalasok[i]
                return "Foglalás lemondva."
        return "Nincs ilyen foglalás."

    def listaz_foglalasok(self):
        if not self.foglalasok:
            return "Nincsenek foglalások."
        return '\n'.join(f"Szobaszám: {f['szobaszam']}, Dátum: {f['datum']}, Ár: {f['ar']} Ft" for f in self.foglalasok)

class SzallodaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Szalloda Kezelő")
        self.geometry("600x500")
        self.configure(bg='gray')
        self.iconbitmap('icon.ico')

        self.szalloda = Szalloda("Best Hotel")
        self.szalloda.szoba_hozzaad(EgyagyasSzoba(101, 15000))
        self.szalloda.szoba_hozzaad(KetagyasSzoba(102, 20000))
        self.szalloda.szoba_hozzaad(KetagyasSzoba(103, 22000))
        self.foglalas_kezelo = Foglalas()

        #Kezdeti feltöltött foglalások
        self.foglalas_kezelo.foglal(self.szalloda, 101, "2024-05-20")
        self.foglalas_kezelo.foglal(self.szalloda, 102, "2024-05-21")
        self.foglalas_kezelo.foglal(self.szalloda, 103, "2024-05-22")
        self.foglalas_kezelo.foglal(self.szalloda, 101, "2024-05-23")
        self.foglalas_kezelo.foglal(self.szalloda, 102, "2024-05-24")

        #Welcome szöveg
        self.label = Label(self, text="Üdvözöljük a Szalloda Kezelő rendszerben!\nTovábbi lehetőségek eléréséhez nyomjon a bal felső sarokba található '🔑'-ikonra!", font=("", 12), bg="gray")
        self.label.pack(pady=100)

        #Lenyíló menü
        self.menu_button = Button(self, text="🔑", font=("Helvetica", 14), command=self.show_menu, bg="gray", fg="white", relief='flat')
        self.menu_button.place(x=10, y=10)

        self.menu = Menu(self, bg="gray", fg="white", tearoff=0)
        self.menu.add_command(label="Foglalás", command=self.foglalas)
        self.menu.add_command(label="Lemondás", command=self.lemondas)
        self.menu.add_command(label="Foglalások Listázása", command=self.listazas)
        self.menu.add_separator()
        self.menu.add_command(label="Kilépés", command=self.quit)

    def show_menu(self):
        self.menu.post(self.menu_button.winfo_rootx(), self.menu_button.winfo_rooty() + self.menu_button.winfo_height())

    def foglalas(self):
        szobaszam = simpledialog.askinteger("Foglalás", "Adja meg a szobaszámot:")
        datum = simpledialog.askstring("Foglalás", "Adja meg a foglalás dátumát (éééé-hh-nn):")
        eredmeny = self.foglalas_kezelo.foglal(self.szalloda, szobaszam, datum)
        messagebox.showinfo("Foglalás Eredménye", eredmeny)

    def lemondas(self):
        szobaszam = simpledialog.askinteger("Lemondás", "Adja meg a szobaszámot:")
        datum = simpledialog.askstring("Lemondás", "Adja meg a lemondás dátumát (éééé-hh-nn):")
        eredmeny = self.foglalas_kezelo.lemond(szobaszam, datum)
        messagebox.showinfo("Lemondás Eredménye", eredmeny)

    def listazas(self):
        foglalasok = self.foglalas_kezelo.listaz_foglalasok()
        messagebox.showinfo("Foglalások Listája", foglalasok)

if __name__ == "__main__":
    app = SzallodaApp()
    app.mainloop()