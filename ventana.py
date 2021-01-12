import tkinter as tk
from tkinter import filedialog
import matplotlib
from numpy import arange, sin, pi, cos
import math
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import archivo as Arch
import datetime as dt



class Application(tk.Frame):
    def __init__(self, root):

        tk.Frame.__init__(self, root)

        # options for buttons
        button_opt = {'fill': tk.constants.BOTH, 'padx': 5, 'pady': 5}

        # define buttons
        tk.Button(self, text='askdirectory', command=self.processdirectory).pack(**button_opt)
        tk.Button(self, text='askopenfile', command=self.processfile).pack(**button_opt)
        tk.Button(self, text='asksaveasfile', command=self.asksaveasfile).pack(**button_opt)
        tk.Button(self, text='exit', command=self.quit).pack(**button_opt)

        # define options for opening a file
        self.file_opt = options = {}
        options['defaultextension'] = '.csv'
        options['filetypes'] = [('all files', '.csv'), ('csv files', '.csv')]
        options['initialdir'] = './'
        options['parent'] = root
        options['title'] = 'Abrir'

        # define options for saving a file
        self.file_opt1 = options1 = {}
        options1['defaultextension'] = '.txt'
        options1['filetypes'] = [('all files', '.txt'), ('text files', '.txt')]
        options1['initialdir'] = './'
        options1['initialfile'] = 'mes_1_dia_1_al_dia_30.txt'
        options1['parent'] = root
        options1['title'] = 'Guardar'

        # defining options for opening a directory
        self.dir_opt = options = {}
        options['initialdir'] = 'C:\\'
        options['mustexist'] = False
        options['parent'] = root
        options['title'] = 'Abrir carpeta'

    def __askdirectory(self):

        """Returns a selected directoryname."""

        return filedialog.askdirectory(**self.dir_opt)

    def processdirectory(self):
        try:
            path = self.__askdirectory()
            carpeta = Arch.Carpeta(path)
            dic, fm, cm = carpeta.procesar()
            if not (fm == "None"):
                print("La fehca de mayor consumo fue {}, su consumo fue de {}W".format(str(fm), cm))
            My_ventana(fm, cm, dic[fm][1], dic[fm][2])
        except:
            print('Error: la carpeta esta vacia')

    def __askopenfile(self):

        """Returns an opened file in read mode."""

        return filedialog.askopenfile(mode='r', **self.file_opt)

    def processfile(self):
        path = self.__askopenfile().name
        print(path)
        file = Arch.Archivo(path=path)
        co, f = file.maxconsumo()
        print("fecha", co, "consumo", f)
        ventana()

    def asksaveasfile(self):

        """Returns an opened file in write mode."""

        return filedialog.asksaveasfile(mode='w', **self.file_opt1)


def My_ventana(name, mayor, fechas, demanda):
    def Borrar_fig():
        # Matplotlib en Canvas
        f.clf()
        dataPlot.draw()

    master = tk.Tk()
    master.title("Matplotlib-in-Canvas")

    # Lienzo
    cv = tk.Canvas(master, width=800, height=800)
    cv.pack(side=tk.LEFT)

    # recuadro en ventana ppal
    frame = tk.Frame(master)
    frame.pack(side=tk.RIGHT, fill=tk.BOTH)

    # botones en frame
    # pushbutton
    b = tk.Button(frame, text='Quit', command=master.destroy)
    b.pack()

    # static text
    l = tk.Label(frame, text=("la demanda maxima se dio el\n" + name + "\ny fue de " + str(mayor) + "W"))
    l.pack()

    # marco de Matplotlib in Canvas tkinter

    f = Figure(figsize=(12, 8), dpi=100)
    dataPlot = FigureCanvasTkAgg(f, master=cv)
    dataPlot.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    Borrar_fig()
    # Matplotlib en Canvas
    a1 = f.add_subplot(111)
    a1.plot(fechas, demanda, label="demanda")
    f = dt.datetime.strptime(name, "%Y-%m-%d %H:%M:%S")
    a1.plot(f, mayor, "o", label="Maximo")
    a1.legend()
    dataPlot.draw()

    master.mainloop()

def ventana():
    # Construcción de la ventana y sus controles
    ventana = tk.Tk()  # Ventana principal
    ventana.title("Crear gráfica!")

    # Frame para agregar los entry y el botón
    fr_datos_entrada = tk.Frame(ventana)
    fr_datos_entrada.grid(row=0, column=0)

    # dia inicial
    lbl_ini = tk.Label(fr_datos_entrada, text="dia inicial:")
    lbl_ini.grid(column=0, row=0)

    var_init = tk.StringVar(value='1')
    ent_init = tk.Entry(fr_datos_entrada, textvariable=var_init)
    ent_init.grid(column=1, row=0)

    # dia final
    lbl_fin = tk.Label(fr_datos_entrada, text="dia final:")
    lbl_fin.grid(column=0, row=1)

    var_fin = tk.StringVar(value='30')
    ent_fin = tk.Entry(fr_datos_entrada, textvariable=var_fin)
    ent_fin.grid(column=1, row=1)

    # Botón graficar
    boton = tk.Button(fr_datos_entrada, text="Graficar")
    boton.grid(column=1, row=2)
    # Ejecuto la aplicación
    ventana.mainloop()


# def ventana2():
#     master = tk.Tk()
#     master.title("Matplotlib-in-Canvas")
#
#     # Lienzo
#     cv = tk.Canvas(master, width=800, height=800)
#     cv.pack(side=tk.LEFT)
#
#     # recuadro en ventana ppal
#     frame = tk.Frame(master)
#     frame.pack(side=tk.RIGHT, fill=tk.BOTH)
#
#     # botones en frame
#     # pushbutton
#     b = tk.Button(frame, text='Quit', command=master.destroy)
#     b.pack()
#
#     # static text
#     l = tk.Label(frame, text="hola")
#     l.pack()
#
#     # marco de Matplotlib in Canvas tkinter
#
#     f = Figure(figsize=(12, 8), dpi=100)
#     dataPlot = FigureCanvasTkAgg(f, master=cv)
#     dataPlot.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
#     Borrar_fig()
#     # Matplotlib en Canvas
#     a1 = f.add_subplot(111)
#     a1.plot(fechas, demanda, label="demanda")
#     a1.legend()
#     dataPlot.draw()
#
#     master.mainloop()


if __name__ == '__main__':
    raiz = tk.Tk()
    Application(raiz).pack()
    raiz.mainloop()
