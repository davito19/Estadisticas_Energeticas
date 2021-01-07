import tkinter as tk
from tkinter import filedialog
import archivo as Arch


class Application(tk.Frame):
    def __init__(self, root):

        tk.Frame.__init__(self, root)

        # options for buttons
        button_opt = {'fill': tk.constants.BOTH, 'padx': 5, 'pady': 5}

        # define buttons
        tk.Button(self, text='askdirectory', command=self.processdirectory).pack(**button_opt)
        tk.Button(self, text='askopenfile', command=self.processfile).pack(**button_opt)
        tk.Button(self, text='asksaveasfile', command=self.asksaveasfile).pack(**button_opt)
        tk.Button(self, text='asksaveasfilename', command=self.asksaveasfilename).pack(**button_opt)
        tk.Button(self, text='exit', command=self.quit).pack(**button_opt)

        # define options for opening a file
        self.file_opt = options = {}
        options['defaultextension'] = '.csv'
        options['filetypes'] = [('all files', '.csv'), ('csv files', '.csv')]
        options['initialdir'] = 'C:\\'
        options['parent'] = root
        options['title'] = 'Abrir'

        # define options for saving a file
        self.file_opt1 = options1 = {}
        options1['defaultextension'] = '.txt'
        options1['filetypes'] = [('all files', '.txt'), ('text files', '.txt')]
        options1['initialdir'] = 'C:\\'
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
        path = self.__askdirectory()
        print(path)
        carpeta = Arch.Carpeta(path)
        _, fm, cm = carpeta.procesar()
        print("La fehca de mayor consumo fue {}, su consumo fue de {}W".format(str(fm), cm))

    def __askopenfile(self):

        """Returns an opened file in read mode."""

        return filedialog.askopenfile(mode='r', **self.file_opt)

    def processfile(self):
        path = self.__askopenfile().name
        print(path)
        file = Arch.Archivo(path=path)
        co, f = file.maxconsumo()
        print("fecha", co, "consumo", f)

    def asksaveasfile(self):

        """Returns an opened file in write mode."""

        return filedialog.asksaveasfile(mode='w', **self.file_opt1)

    def asksaveasfilename(self):

        """Returns an opened file in write mode.
        This time the dialog just returns a filename and the file is opened by your own code.
        """

        # get filename
        filename = filedialog.asksaveasfilename(**self.file_opt1)

        # open file on your own
        if filename:
            return open(filename, 'w')


if __name__ == '__main__':
    raiz = tk.Tk()
    Application(raiz).pack()
    raiz.mainloop()
