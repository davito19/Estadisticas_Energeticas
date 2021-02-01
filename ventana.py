from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from archivo import Carpeta, Archivo
import datetime as dt


class Aplicacion:
    def __init__(self):
        self.raiz = Tk()
        self.raiz.title("Demandas Energeticas")

        # Declara variables de control

        self.path_dir = "./"
        self.path_file = None
        self.file = None
        self.nameout = None

        self.ini = IntVar(value=1)
        self.fin = DoubleVar(value=30)
        self.total = StringVar(value='wait...')

        # Carga imagen para asociar a widget Label()

        tren = PhotoImage(file='torre.png')

        # Declara widgets de la ventana
        # Se incluye el widget de tipo Button 'Calcular' que utiliza
        # la opción 'command' para validar datos y calcular el
        # importe a pagar cuando sea presionado

        self.boton0 = ttk.Button(self.raiz, text=" Procesar Carpeta de Registros",
                                 command=self.procesardir)

        self.boton = ttk.Button(self.raiz, text="Abrir Registro",
                                command=self.procesafile)

        self.separ0 = ttk.Separator(self.raiz, orient=HORIZONTAL)

        self.imagen1 = ttk.Label(self.raiz, image=tren,
                                 anchor="center")

        self.etiq3 = ttk.Label(self.raiz,
                               text="Día inicial:")
        self.dist = ttk.Entry(self.raiz, textvariable=self.ini,
                              width=10)
        self.etiq4 = ttk.Label(self.raiz, text="Dia final:")
        self.coste = ttk.Entry(self.raiz, textvariable=self.fin,
                               width=10)
        self.etiq5 = ttk.Label(self.raiz, text="Terminal:")
        self.etiq6 = ttk.Label(self.raiz, textvariable=self.total,
                               foreground="yellow", background="black",
                               borderwidth=5, anchor="e")
        self.separ1 = ttk.Separator(self.raiz, orient=HORIZONTAL)

        self.boton1 = ttk.Button(self.raiz, text="Guardar",
                                 command=self.save)
        self.boton2 = ttk.Button(self.raiz, text="Salir",
                                 command=quit)

        # empaquetado
        self.imagen1.pack(side=TOP, fill=BOTH, expand=True,
                          padx=10, pady=5)
        self.boton0.pack(side=TOP, fill=BOTH, expand=True,
                         padx=10, pady=10)
        self.boton.pack(side=TOP, fill=BOTH, expand=True,
                        padx=10, pady=10)
        self.separ0.pack(side=TOP, fill=BOTH, expand=True,
                         padx=5, pady=5)

        self.etiq3.pack(side=TOP, fill=BOTH, expand=True,
                        padx=10, pady=5)
        self.dist.pack(side=TOP, fill=X, expand=True,
                       padx=20, pady=5)
        self.etiq4.pack(side=TOP, fill=BOTH, expand=True,
                        padx=10, pady=5)
        self.coste.pack(side=TOP, fill=X, expand=True,
                        padx=20, pady=5)
        self.etiq5.pack(side=TOP, fill=BOTH, expand=True,
                        padx=10, pady=5)
        self.etiq6.pack(side=TOP, fill=BOTH, expand=True,
                        padx=20, pady=5)
        self.separ1.pack(side=TOP, fill=BOTH, expand=True,
                         padx=5, pady=5)
        self.boton1.pack(side=LEFT, fill=BOTH, expand=True,
                         padx=10, pady=10)
        self.boton2.pack(side=RIGHT, fill=BOTH, expand=True,
                         padx=10, pady=10)
        self.raiz.mainloop()

    def __askdirectory(self):

        """Returns a selected directoryname."""
        self.path_dir = filedialog.askdirectory()

    def procesardir(self):
        self.__askdirectory()
        try:
            carpeta = Carpeta(self.path_dir)
            dic, fm, cm = carpeta.procesar()
            if fm != "None":
                self.total.set("Carpeta procesada")
                self.grafica_emergente(fm, cm, dic[fm][1], dic[fm][2])
            else:
                self.total.set("No se encontraron archivos a procesar")
        except:
            self.total.set("No hay carpeta a procesar")

    def grafica_emergente(self, name, mayor, fechas, demanda):
        def Borrar_fig():
            # Matplotlib en Canvas
            f.clf()
            dataPlot.draw()

        master = Tk()
        master.title("Mes con mayor demanda")

        # Lienzo
        cv = Canvas(master, width=800, height=800)
        cv.pack(side=LEFT)

        # recuadro en ventana ppal
        frame = Frame(master)
        frame.pack(side=RIGHT, fill=BOTH)

        # botones en frame
        # pushbutton
        b = ttk.Button(frame, text='Quit', command=master.destroy)
        b.pack()

        # static text
        l = ttk.Label(frame, text=("la demanda maxima se dio el\n" + name + "\ny fue de " + str(mayor) + "W"))
        l.pack()

        # marco de Matplotlib in Canvas tkinter

        f = Figure(figsize=(12, 8), dpi=100)
        dataPlot = FigureCanvasTkAgg(f, master=cv)
        dataPlot.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        Borrar_fig()
        # Matplotlib en Canvas
        a1 = f.add_subplot(111)
        a1.plot(fechas, demanda, label="demanda")
        f = dt.datetime.strptime(name, "%Y-%m-%d %H:%M:%S")
        a1.plot(f, mayor, "o", label="Maximo")
        a1.legend()
        dataPlot.draw()

        master.mainloop()

    def __askopenfile(self):
        try:
            self.path_file = filedialog.askopenfile(filetypes=(('All files', '.*'), ('csv files', '.csv'))).name
        except:
            self.path_file = None

    def procesafile(self):
        self.__askopenfile()
        if self.path_file is None:
            self.total.set("No hay archivo a procesar")
        else:
            self.file = Archivo(path=self.path_file)
            self.total.set("Archivo listo a procesar")

    def grafica_file(self):
        def Borrar_fig():
            # Matplotlib en Canvas
            f.clf()
            dataPlot.draw()

        master = Tk()
        master.title("Grafica de archivo procesado")

        # Lienzo
        cv = Canvas(master, width=800, height=800)
        cv.pack(side=LEFT)

        # recuadro en ventana ppal
        frame = Frame(master)
        frame.pack(side=RIGHT, fill=BOTH)

        # botones en frame
        # pushbutton
        b = ttk.Button(frame, text='Quit', command=master.destroy)
        b.pack()

        # marco de Matplotlib in Canvas tkinter

        f = Figure(figsize=(12, 8), dpi=100)
        dataPlot = FigureCanvasTkAgg(f, master=cv)
        dataPlot.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        Borrar_fig()
        # Matplotlib en Canvas
        a1 = f.add_subplot(111)
        fechas, demanda = self.file.procesar(int(self.ini.get()), int(self.fin.get()))
        a1.plot(fechas, demanda, label="demanda")
        a1.legend()
        dataPlot.draw()

        master.mainloop()

    def __asksavefile(self):
        """
        Función encargada de crear un archivo a guardar
        """
        try:    # En caso de que se cree un archivo al guardar
            # modificamos el atributo nameout con la ruta del archivo creado
            self.nameout = filedialog.asksaveasfile(filetypes=(('All files', '.*'), ('text files', '.txt'))
                                                    , initialfile='mes_1_del_dia_1_al_30.txt').name
        except:     # En caso de error
            # modificamos el atributo nameout con None
            self.nameout = None

    def save(self):
        """
        Funcion llamada cuando se presiona el boton guardar
        """
        if self.file is None:  # Se verifica si existe un registro de la demanda en colombia abierto
            self.total.set("No hay registro abierto")  # Muestra en el widget entry informacion para el usuario
        else:
            self.__asksavefile()  # En caso de que exista un archivo abierto, pregunto el nombre del archivo a guardar
            if self.nameout is None:  # Si no se ingresan los datos correctos
                self.total.set("Ingrese el nombre del archivo a guardar")  # Muestra un mensaje para el usuario
            else:  # si se ingresa un archivo a guardar
                if 1 <= self.ini.get() < self.fin.get() <= 30:  # verifico si el rango de dias ingresados por el usuario
                    self.total.set("Registro procesado y guardado")  # Muestra un mensaje para el usuario
                    # proceso y escribo el archivo de salida
                    self.file.escribr(self.nameout, True, int(self.ini.get()), int(self.fin.get()))
                    self.grafica_file()  # Grafico el archivo procesado
                else: # En caso de que el rango de dias se invalido
                    self.total.set("Rango de fechas incorrectos")   # Muestro un mensaje al usuario
                    # Establezco un rango de dias validos
                    self.ini.set(1)
                    self.fin.set(10)


# if __name__ == '__main__':
#     mi_app = Aplicacion()
