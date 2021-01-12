import os
import datetime as dt


class Archivo:
    def __init__(self, name: str = None, base_dir: str = None, path=None):
        """
        Constructor de la clase Archivo

        :param name: string que contiene el nombre del archivo
        :param base_dir: string que contiene el directorio raiz del archivo
        """

        if not (name is None):
            self.name = name  # Se asigna el atributo de name a la clase
            self.base_dir = base_dir  # Se asigna el atributo de base_dir a la clase
            self.path = os.path.join(base_dir, name)  # Se asigna el atributo de path a la clase
        else:
            self.path = path

    def __str__(self):
        """
        Convierte un objeto de la clase archivo a string

        :return: retorna el string de la clase Archivo
        """
        assert isinstance(self, Archivo), "El atributo debe ser tipo Archivo"
        return "Archivo: {} Ruta: {}".format(self.name, self.base_dir)

    def leer(self):
        """
        Lee y procesa el archivo

        :return: fechas: list, que contiene las fechas de consumo del mes
        :return: demanda: list, que contiene los consumos del mes
        """
        assert isinstance(self, Archivo), "El atributo debe ser tipo Archivo"
        data = open(self.path)  # Se abre el archivo a procesar
        data.readline().split(";")  # se lee el encabezado sin asignar, para mover el cursor a los datos

        # Variables Auxiliares
        demanda = []  # Almacena el consumo energetico del mes
        fechas = []  # Almacena las fechas y horas de consumo

        # Se recorre cada linea del archivo y se extraen sus valores
        for datos in data:
            datos = datos.split(";")  # Se guardan los valores de la linea leída separandolos por ;

            fecha = datos[2]  # Se almacenan de la segunda columna la fecha, correspondiente a un dia de consumo
            demanda_dia = datos[4:28]  # Se almacenan los 24 valores de consumos cada valor representa una hora del día

            horas = []  # Variable para construir un vector de horas

            for i in range(0, len(demanda_dia)):
                demanda_dia[i] = float((demanda_dia[i].replace(",", ".")))  # Convertimos el vector de str a vector int
                horas.append(
                    dt.datetime.strptime(fecha + " " + str(i), "%Y-%m-%d %H"))  # Construimos el vector de horas

            demanda.extend(demanda_dia)  # Añadimos el consumo de un día a la demanda total del mes
            fechas.extend(horas)  # Añadimos la fecha del dia de consumo con sus 24 horas

        data.close()  # Cerramos el archivo
        return fechas, demanda  # retornamos la fecha y el consumo

    def maxconsumo(self):
        """
        Metodo para determinar la demanda maxima y la fecha de ocurrencia de un archivo sobre consumo energetico

        :return: retorna una tupla con la fecha de maximo consumo y el valor maximo de consumo
        fecha_m, fecha de maximo consumo
        mayor, maximo consumo

        """
        assert isinstance(self, Archivo), "El atributo debe ser tipo Archivo"
        mayor = 0
        fecha_m = "None"
        fechas, demanda = self.leer()

        for i in range(len(demanda)):
            if demanda[i] >= mayor:  # determina el nuevo valor de mayor consumo
                fecha_m = fechas[i]  # guarda el mayor consumo
                mayor = demanda[i]  # guarda la fecha de mayor consumo

        return fecha_m, mayor  # retornamos la fecha y el consumo

    def procesar(self, rango_inf: int, rango_sup: int):
        """
        Procesa la información del archivo y retorna los valores solictados en el intervalo de fechas correspondientes
        :param rango_inf: Limite inferior del rango de fechas a procesar
        :param rango_sup: Limite superior del rango de fechas a procesar
        :return: una tupla de listas con las fechas y los consumos deseados
        """
        assert isinstance(self, Archivo), "El atributo debe ser tipo Archivo"
        data = open(self.path)  # abre el archivo

        data.readline().split(";")  # leo la primera linea o encabezado

        demanda_mes = []  # variable donde se guardan los datos del consumo del intervalo seleccionado
        fecha_hora_mes = []  # variable donde se guardan los datos de las fechas consumo del intervalo seleccionado

        for datos in data:  # recorro las lineas de mi archivo
            datos = datos.split(";")  # obtengo una lista de los datos que estan en un string separados por ;

            fecha = datos[2]  # guardo la fecha del dia procesado
            # extraigo la fecha para determinar si el dia esta en el rango de interes
            dia = dt.datetime.strptime(fecha,
                                       "%Y-%m-%d")

            if rango_inf <= dia.day <= rango_sup:  # determino si el dia esta en el rango de interes
                demanda_dia = datos[4:28]  # obtengo los datos de consumo
                fecha_hora_dia = []
                for i in range(len(demanda_dia)):
                    demanda_dia[i] = float(demanda_dia[i].replace(",", "."))  # convierto a float el consumo
                    # lista con la fecha correspondiente al consumo
                    fecha_hora_dia.append(dt.datetime.strptime(fecha + " " + str(i),
                                                               "%Y-%m-%d %H"))

                demanda_mes.extend(
                    demanda_dia)  # Añado los consumos del dia de interes a todos los datos de consumo de interes
                fecha_hora_mes.extend(
                    fecha_hora_dia)  # añado las fecha del día de interes a todos los datos de fechas de interes

        data.close()  # cierro el archivo

        return fecha_hora_mes, demanda_mes

    def escribr(self, name: str = "default.txt", process: bool = True, rango_inf: int = -1, rango_sup: int = -1,
                fecha=None, consumo=None):
        """
        Escribe un archivo con los datos de consumo procesados

        :param name: nombre del archivo a escribir
        :param process: boolean, si es verdadero realiza el procesamiento del archivo y lo escribe en caso contrario
                        solo escribe los datos ya procesados
        :param rango_inf: int, en caso de que process sea verdadero establece el dia inicial desde donde se escribe
                          el archivo
        :param rango_sup: int, en caso de que process sea verdadero establece el dia final desde donde se escribe
                          el archivo
        :param fecha: list or tuple, con las fechas ya procesadas
        :param consumo: list or tuple, con los consumos ya procesadas
        """
        # if fecha is None:
        #     fecha = []
        # if consumo is None:
        #     consumo = []
        assert isinstance(self, Archivo), "El atributo debe ser tipo Archivo"
        if process and rango_sup > rango_inf >= 0:
            fecha, consumo = self.procesar(rango_inf, rango_sup)  # Proceso el archivo entre los dias dados
            data = open(name, "w")  # abro el archivo txt si existe o lo creo en caso de que no
            for i in range(0, len(consumo)):  # Recorro el arreglo de valores a escribir en el archivo
                data.write(str(fecha[i]))  # Escribo la fecha
                data.write("; ")  # Separador
                data.write(str(consumo[i]) + "\n")  # Escribo la demanda y salto de linea
            data.close()  # cierro el archivo
            print("se escribio el archivo " + name + " del dia_{}_al_{} con los datos respectivos".format(9, rango_inf,
                                                                                                          rango_sup))

        elif not process:
            data = open(name, "w")  # abro el archivo txt si existe o lo creo en caso de que no
            for i in range(0, len(consumo)):  # Recorro el arreglo de valores a escribir en el archivo
                data.write(str(fecha[i]))  # Escribo la fecha
                data.write("; ")  # Separador
                data.write(str(consumo[i]) + "\n")  # Escribo la demanda y salto de linea
            data.close()  # cierro el archivo
            print("se escribio el archivo  con los datos respectivos")


class Carpeta:
    def __init__(self, path: str):
        """
        Constructor de la clase Carpeta

        :param path: str, que contiene la ruta de la carpeta
        """
        self.path = path  # Atributo de ruta de la carpeta
        self.list_files = os.listdir(path)  # Atributo de los elementos de la carpeta
        self.files_csv = self.archivoscsv()  # Atributo de los elementos csv de la carpeta

    def __str__(self):
        """
        Convierte un objeto de la clase Carpeta a string

        :return: retorna el string de la clase Carpeta
        """
        assert isinstance(self, Carpeta), "El atributo debe ser tipo Carpeta"
        return "Ruta: {}".format(self.path)

    def archivoscsv(self):
        """
        Encuentra los archivos csv del directorio
        :return: Retorna un diccionario con todos los archivos csv que se pueden procesar
        """
        csv = {}  # Diccionario donde se almacenan los elementos
        idx = 1  # Claves para el diccionarios
        for i in range(0, len(self.list_files)):  # iteramos sobre todos los elementos en la carpeta
            if self.list_files[i].lower().endswith(".csv"):  # Si el archivo es csv
                csv[str(idx)] = self.list_files[i]  # lo almacenamos en el diccionario
                idx += 1  # aumentamos el valor de la clave
        return csv  # Retornamos el archivo csv

    def procesar(self):
        """
        procesa los elementos csv de la carpeta
        :return: dic: diccionario con el maximo de consumo de cada archivo procesado, sus fechas y sus consumos
        :return: fecha: str, fecha del mes con mayor consumo, sirve de clave para extraer sus valores de dic.
        :return: mayor: int, con el valor de consumo maximo de los archivo procesados.
        """
        dic = {}  # diccionario de listas, contendra el maximo consumo del mes y todos los datos del mes
        mayor = 0  # Variable que contendra el valor de consumo maximo
        fecha = "None"  # Variable tipo str que contendra la fecha de mayor consumo
        for i in self.files_csv:  # Iteramos sobre todos los archivos a procesar
            file = Archivo(self.files_csv[i], self.path)  # creamos un objeto de la clase archivo
            fecha, maximo = file.maxconsumo()  # extraemos la demanda maxima y su fecha del objeto archivo
            mes, consumo = file.leer()  # procesamos el archivo
            dic[str(fecha)] = [maximo, mes, consumo]  # construimos el diccionario para cada archivo

        for i in dic:  # Recorremos el diccionario
            if dic[i][0] >= mayor:  # determinamos el archivo con mayor consumo
                mayor = dic[i][0]  # asignamos el valor de mayor consumo
                fecha = i  # Guardamos la clave del mes de mayor consumo

        return dic, fecha, mayor  # retornamos los valores de interes


if __name__ == '__main__':
    file = Archivo("MC-SIN-OFI-DR-Julio-2020.csv", "./")
    print(file)
    print(type(file))
    co, f = file.maxconsumo()
    print("fecha", co, "consumo", f)
    dos, uno = file.procesar(5, 8)
    file.escribr("hola.txt", False, fecha=dos, consumo=uno)

    carpeta = Carpeta("./")
    print(carpeta.path)
    print(carpeta.list_files)
    print(carpeta.files_csv)
    dicc, fm, m = carpeta.procesar()
    print(fm, m)
    print(dicc[fm][0])
