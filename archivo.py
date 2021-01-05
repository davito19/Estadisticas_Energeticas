import os
import datetime as dt


class Archivo:
    def __init__(self, name: str, base_dir: str):
        """
        Constructor de la clase Archivo

        :param name: string que contiene el nombre del archivo
        :param base_dir: string que contiene el directorio raiz del archivo
        """
        self.name = name    # Se asigna el atributo de name a la clase
        self.base_dir = base_dir    # Se asigna el atributo de base_dir a la clase
        self.path = os.path.join(base_dir, name)    # Se asigna el atributo de path a la clase

    def __str__(self):
        """
        Convierte un objeto de la clase archivo a string

        :return: retorna el string de la clase Archivo
        """
        assert isinstance(self, Archivo), "El atributo debe ser tipo Archivo"
        return "Archivo: {} Ruta: {}".format(self.name, self.base_dir)

    def maxconsumo(self):
        """
        Metodo para determinar la demanda maxima y la fecha de ocurrencia de un archivo sobre consumo energetico

        :return: retorna una tupla con la fecha de maximo consumo y el valor maximo de consumo
        fecha_m, fecha de maximo consumo
        mayor, maximo consumo

        """
        data = open(self.path)  # Se abre el archivo a procesar
        data.readline().split(";")  # se lee el encabezado sin asignar, para mover el cursor a los datos

        # Variables Auxiliares
        demanda = []    # Almacena el consumo energetico del mes
        fechas = []     # Almacena las fechas y horas de consumo
        fecha_m = 0     # Almacena la fecha de mayor consumo
        mayor = 0       # Almacena el mayor consumo

        # Se recorre cada linea del archivo y se extraen sus valores
        for datos in data:
            datos = datos.split(";")

            fecha = datos[2]

            demanda_dia = datos[4:28]
            horas = []

            for i in range(0, len(demanda_dia)):
                demanda_dia[i] = float((demanda_dia[i].replace(",", ".")))
                horas.append(dt.datetime.strptime(fecha + " " + str(i), "%Y-%m-%d %H"))

            demanda.extend(demanda_dia)
            fechas.extend(horas)

        for i in range(len(demanda)):
            if demanda[i] >= mayor:  # determina el nuevo valor de mayor consumo
                fecha_m = fechas[i]  # guarda el mayor consumo
                mayor = demanda[i]  # guarda la fecha de mayor consumo

        data.close()
        return fecha_m, mayor

    def procesar(self, rango_inf: int, rango_sup: int):
        file = open(self.path)  # abro el archivo

        enc = file.readline()  # leo la primera linea o encabezado
        enc = enc.split(";")

        demanda_mes = []
        fecha_hora_mes = []

        for datos in file:  # recorro las lineas de mi archivo
            # datos=file.readline()
            datos = datos.split(";")  # obtengo una lista de los datos que estan en un string separados por ;

            # guardo la fecha del dia procesado
            fecha = datos[2]
            dia = dt.datetime.strptime(fecha,
                                       "%Y-%m-%d")  # extraigo la fecha para determinar si el dia esta en el rango de interes
            # print(dia.day)
            if dia.day >= rango_inf and dia.day <= rango_sup:  # determino si el dia esta en el rango de interes
                demanda_dia = datos[4:28]  # obtengo los datos de consumo
                fecha_hora_dia = []
                for i in range(len(demanda_dia)):
                    demanda_dia[i] = float(demanda_dia[i].replace(",", "."))  # convierto a float el consumo
                    fecha_hora_dia.append(dt.datetime.strptime(fecha + " " + str(i),
                                                               "%Y-%m-%d %H"))  # lista con la fecha correspondiente al consumo

                demanda_mes.extend(
                    demanda_dia)  # Añado los consumos del dia de interes a todos los datos de consumo de interes
                fecha_hora_mes.extend(
                    fecha_hora_dia)  # añado las fecha del día de interes a todos los datos de fechas de interes

        file.close()  # cierro el archivo

        return fecha_hora_mes, demanda_mes

    def escribr(self, process: bool = True, rango_inf: int = -1, rango_sup: int = -1, fecha: list = [],
                consumo: list = []):

        if process and rango_sup > rango_inf >= 0:
            fecha, consumo = self.procesar(rango_inf, rango_sup)
            file = open("mes_{}_dia_{}_al_{}.txt".format(9, rango_inf, rango_sup),
                        "w")  # abro el archivo txt si existe o lo creo en caso de que no
            for i in range(0, len(consumo)):  # Recorro el arreglo de valores a escribir en el archivo
                file.write(str(fecha[i]))  # Escribo la fecha
                file.write("; ")  # Separador
                file.write(str(consumo[i]) + "\n")  # Escribo la demanda y salto de linea
            file.close()
            print("se escribio el archivo mes_{}_dia_{}_al_{}.txt con los datos respectivos".format(9, rango_inf,
                                                                                                    rango_sup))  # cierro el archivo

        elif not process:
            file = open("mes_9_dia_5_al_8.txt",
                        "w")  # abro el archivo txt si existe o lo creo en caso de que no
            for i in range(0, len(consumo)):  # Recorro el arreglo de valores a escribir en el archivo
                file.write(str(fecha[i]))  # Escribo la fecha
                file.write("; ")  # Separador
                file.write(str(consumo[i]) + "\n")  # Escribo la demanda y salto de linea
            file.close()
            print("se escribio el archivo  con los datos respectivos")  # cierro el archivo


if __name__ == '__main__':
    file = Archivo("MC-SIN-OFI-DR-Septiembre-2020.csv", "./")
    print(file)
    print(type(file))
    print(file.maxconsumo())
    dos, uno = file.procesar(5, 8)
    file.escribr(False, fecha=dos, consumo=uno)
