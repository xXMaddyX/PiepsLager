import ttkbootstrap as ttk
import threading
import tkinter as tk
import tkinter.filedialog as filedialog
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.tableview import *
from PIL import Image, ImageTk
import csv


class MainWindow(ttk.Window):
    def __init__(self, *args, **kwargs):
        ttk.Window.__init__(self, *args, **kwargs)
        self.title("Piep´s Archery Warehouse")
        self.geometry("1400x800")
        self.minsize(1400, 800)
        self.maxsize(1400, 800)
        self.place_window_center()

        #Image
        self.image = Image.open("Logo.png").resize((250, 200))
        self.photo = ImageTk.PhotoImage(self.image)


        # Data Store Vari
        self.data = []
        

        # Set Mainbar
        self.navbar = ttk.Frame(self, padding="5 10", style="TButton", height=10)
        self.navbar.pack(side="top", fill="x")

        #info Label
        my_font = ttk.font.Font(size=15)
        self.info_label = ttk.Label(self, text="Artikel", font=my_font)
        self.info_label.pack(side="top")

        # Navbar Buttons
        self.navbar_button1 = ttk.Menubutton(self.navbar, text="Datei")
        self.navbar_button1.pack(side="left", padx=10)
        self.create_dropdown(self.navbar_button1)

        self.calc_button = ttk.Button(self.navbar, text="Zoll Rechner", command=self.init_secound_window)
        self.calc_button.pack(side="left")

         # Add new item Frame
        self.add_item_frame = ttk.Frame(self, padding="10")
        self.add_item_frame.pack(side="left", fill="y")

        # Add new item Labels and Entry widgets
        ttk.Label(self.add_item_frame, text="Artikel:").grid(row=0, column=0, sticky="w")
        self.artikel_entry = ttk.Entry(self.add_item_frame)
        self.artikel_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.add_item_frame, text="Bezeichnung:").grid(row=1, column=0, sticky="w")
        self.bezeichnung_entry = ttk.Entry(self.add_item_frame)
        self.bezeichnung_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.add_item_frame, text="Menge:").grid(row=2, column=0, sticky="w")
        self.menge_entry = ttk.Entry(self.add_item_frame)
        self.menge_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.add_item_frame, text="Artikelnummer:").grid(row=3, column=0, sticky="w")
        self.artikelnummer_entry = ttk.Entry(self.add_item_frame)
        self.artikelnummer_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(self.add_item_frame, text="Hinzufügen", command=self.add_new_item).grid(row=4, column=0, padx=5, pady=10)
        ttk.Button(self.add_item_frame, text="Speichern", command=self.quick_save).grid(row=4, column=1, padx=5, pady=10)
        ttk.Button(self.add_item_frame, text="Bearbeiten", command=self.get_selection).grid(row=5, column=0, padx=5, pady=10)
        ttk.Button(self.add_item_frame, text="Updaten", command=self.update_selelection).grid(row=5, column=1, padx=5, pady=10)




        # Add Table Frame
        self.table_frame = ttk.Frame(self, padding="10")
        self.table_frame.pack(side="right", fill="both", expand=True)

        # Create Table
        self.table = self.create_table()
    
        #photo placement
        photo_label = ttk.Label(self, image=self.photo, text="by Freelance Archery", compound="top")
        photo_label.config()
        photo_label.place(x=0, y=550)

        self.file_path = "tabledata.csv"  # Pfad zur CSV-Datei
        if self.check_file_exists(self.file_path):
            self.load_data_from_file(self.file_path)
        else:
            # Create empty file
            self.save_data_to_file(self.file_path)


        # Create and set function in Dropdown
    def create_dropdown(self, button):
        dropdown = ttk.Menu(button, tearoff=False)
        dropdown.add_command(label="Öffnen", command=self.open_file)
        dropdown.add_command(label="Speichern unter", command=self.save_table)
        dropdown.add_command(label="Beenden", command=self.exit_programm)

        button["menu"] = dropdown

    def init_secound_window(self):
        second_window_thread = threading.Thread(target=SecondWindow)
        second_window_thread.start()

    def get_selection(self):
        selection = self.table.view.selection()
        items = self.table.view.item(selection)
        values = items["values"]
        self.artikel_entry.insert(tk.END, f'{values[0]}')
        self.bezeichnung_entry.insert(tk.END, f'{values[1]}')
        self.menge_entry.insert(tk.END, f'{values[2]}')
        self.artikelnummer_entry.insert(tk.END, f'{values[3]}')

    def update_selelection(self):
        iids = self.table.view.selection()
        if len(iids) > 0:
            prev_item = self.table.view.prev(iids[0])
            self.table.delete_rows(iids=iids)
            self.table.view.focus(prev_item)
            self.table.view.selection_set(prev_item)
            self.add_new_item()

        toast = ToastNotification(
        title="Übermittlung erfolgreich",
        message="Daten erfolgreich Aktualisiert",
        duration=3000
        )
        toast.show_toast()


        # Create Tabel
    def create_table(self):
        coldata = [
            {"text": "Artikel/Material", "width": 300},
            {"text": "Beschreibung", "width": 350},
            {"text": "Menge"},
            {"text": "Artikelnummer", "width": 276},
            ]
        self.table = Tableview(
            master=self,
            rowdata=self.data,
            coldata=coldata,
            paginated=True,
            searchable=True,
            bootstyle=PRIMARY,
            height=25,
            pagesize=25
            )
        self.table.pack(fill="both", expand=True)
        

        # Add Data to Table
        for data_item in self.data:
            self.table.insert_row(data_item)

        return self.table
    
    

        # Get Input to add Item(Row)
    def add_new_item(self):
        artikel = self.artikel_entry.get()
        bezeichnung = self.bezeichnung_entry.get()
        menge = self.menge_entry.get()
        artikelnummer = self.artikelnummer_entry.get()

        # Add new item to data list
        self.data = [row.values for row in self.table.tablerows]
        new_item = (artikel, bezeichnung, menge, artikelnummer)
        self.data.append(new_item)

        # Clear Entry Fields
        self.artikel_entry.delete(0, 'end')
        self.bezeichnung_entry.delete(0, 'end')
        self.menge_entry.delete(0, 'end')
        self.artikelnummer_entry.delete(0, 'end')

        #Toast Popup Notification
        toast = ToastNotification(
            title="Übermittlung erfolgreich",
            message="Daten erfolgreich eingegeben",
            duration=3000
        )
        toast.show_toast()


        # Update Table
        self.table.destroy()
        self.table = self.create_table()


    #save table to csv
    def save_table(self):
            records = [row.values for row in self.table.tablerows]
            self.table.save_data_to_csv(records=records)


    def check_file_exists(self, file_path):
        try:
            with open(file_path, 'r'):
                return True
        except FileNotFoundError:
            return False

    #Save Data to file
    def save_data_to_file(self, file_path):
        with open(file_path, 'w') as file:
            for data_item in self.data:
                file.write(','.join(map(str, data_item)) + '\n')

    #read data from file
    def load_data_from_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                self.data = [tuple(line.strip().split(',')) for line in file.readlines()]
                self.table.destroy()
                self.table = self.create_table()

        except FileNotFoundError:
            #Toast Popup Notification
            toast = ToastNotification(
            title="Warnung",
            message="Keine Datei gefunden",
            duration=3000
            )
            toast.show_toast()


     # Open File
    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV File", "*.CSV"), ("Text File", "*.txt"), ("All Files", "*.*")])
        if file_path:
            print("Datei ausgewählt: " + file_path)
            self.load_data_from_file(file_path)

    # Save File
    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.CSV"), ("All Files", "*.*")])
        if file_path:
            print("Datei gespeichert unter: " + file_path)
            self.save_data_to_file(file_path)

    def quick_save(self):
        records = [row.values for row in self.table.tablerows]
        self.save_to_csv(records=records)

    def save_to_csv(self, records, delimiter=','):
        filename = "tabledata.csv"  # Statischer Dateiname und Pfad
        with open(filename, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter=delimiter)
            writer.writerows(records)

        #Toast Popup Notification
        toast = ToastNotification(
            title="Daten gespeichert",
            message="Daten erfolgreich gespeichert",
            duration=3000
        )
        toast.show_toast()

        # Exit App
    def exit_programm(self):
        self.self.destroy()

    
        


class SecondWindow(ttk.Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x450")
        self.title("Zoll/Cm Calculator")
        self.minsize(400, 430)
        self.maxsize(400, 430)
        self.place_window_center()

        self.font = ttk.font.Font(size=15)

        self.head = ttk.Label(self, background="orange")
        self.head.pack(side="top", fill="x")

        self.head_text = ttk.Label(self.head, text="Zoll/CM Rechner", font=self.font, background="orange", foreground="black")
        self.head_text.pack(side="top")

        self.entry_frame = ttk.Frame(self)
        self.entry_frame.pack(side='top')


        ttk.Label(self.entry_frame).grid(row=0, column=1)
        self.output_widget = ttk.Text(self.entry_frame, font=("Helvetica", 25), height=1, width=10, wrap=tk.WORD)
        self.output_widget.grid(row=0, column=1, pady=20)

        ttk.Label(self.entry_frame, text='Gib einen wert in cm ein').grid(row=1, column=1)
        self.entry_zoll = ttk.Entry(self.entry_frame)
        self.entry_zoll.grid(row=2, column=1, pady=5)

        ttk.Label(self.entry_frame, text='Gib einen wert in Zoll ein').grid(row=4, column=1)
        self.entry_cm = ttk.Entry(self.entry_frame)
        self.entry_cm.grid(row=5, column=1, pady=5)

        ttk.Label(self.entry_frame, text='Gib deine Bogenlänge an um die Sehnenlänge in Zoll zu erhalten').grid(row=7, column=1)
        self.entry_bow = ttk.Entry(self.entry_frame)
        self.entry_bow.grid(row=8, column=1, pady=5)

        ttk.Button(self.entry_frame, text='Berechnen', command=self.output_Zoll).grid(row=3, column=1, pady=5)
        ttk.Button(self.entry_frame, text='Berechnen', command=self.output_cm).grid(row=6, column=1, pady=5)
        ttk.Button(self.entry_frame, text='Berechnen', command=self.output_bow).grid(row=9, column=1, pady=5)


    def data_get_bow(self):
        bow = self.entry_bow.get()
        bow = float(bow) - 3
        self.bow_result = bow

    def output_bow(self):
        self.data_get_bow()
        self.output_widget.delete("1.0", tk.END)
        self.output_widget.insert(ttk.END, f'{self.bow_result} Zoll')  
        self.output_widget.configure(fg="yellow")
        self.output_widget.see(ttk.END)  

    def data_get_cm(self):
        cm = self.entry_cm.get()
        cm = round(float(cm) / 0.3937, 2)
        self.cm_result = cm

    def output_cm(self):
        self.data_get_cm()
        self.output_widget.delete("1.0", tk.END)
        self.output_widget.insert(ttk.END, f'{self.cm_result} cm')  
        self.output_widget.configure(fg="yellow")
        self.output_widget.see(ttk.END)


    def data_get_Zoll(self):
        zoll = self.entry_zoll.get()
        zoll = round(float(zoll) * 0.3937, 2)
        self.zoll_result = zoll

    def output_Zoll(self):
        self.data_get_Zoll()
        self.output_widget.delete("1.0", tk.END)
        self.output_widget.insert(ttk.END, f'{self.zoll_result} Zoll')  
        self.output_widget.configure(fg="yellow")
        self.output_widget.see(ttk.END)  



if __name__ == '__main__':
    app = MainWindow(themename="solar")
    app.mainloop()
