import os
import datetime as dt


class Archivo:
    def __init__(self, name: str, base_dir: str):
        """
        Constructor de la clase Archivo

        :param name: string que contiene el nombre del archivo
        :param base_dir: string que contiene el directorio raiz del archivo
        """
        self.name = name  # Se asigna el atributo de name a la clase
        self.base_dir = base_dir  # Se asigna el atributo de base_dir a la clase
        self.path = os.path.join(base_dir, name)  # Se asigna el atributo de path a la clase

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
        demanda = []  # Almacena el consumo energetico del mes
        fechas = []  # Almacena las fechas y horas de consumo
        fecha_m = 0  # Almacena la fecha de mayor consumo
        mayor = 0  # Almacena el mayor consumo

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

        for i in range(len(demanda)):
            if demanda[i] >= mayor:  # determina el nuevo valor de mayor consumo
                fecha_m = fechas[i]  # guarda el mayor consumo
                mayor = demanda[i]  # guarda la fecha de mayor consumo

        data.close()  # Cerramos el archivo
        return fecha_m, mayor  # retornamos la fecha y el consumo

    def procesar(self, rango_inf: int, rango_sup: int):
        """
        Procesa la información del archivo y retorna los valores solictados en el intervalo de fechas correspondientes
        :param rango_inf: Limite inferior del rango de fechas a procesar
        :param rango_sup: Limite superior del rango de fechas a procesar
        :return: una tupla de listas con las fechas y los consumos deseados
        """
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

        if process and rango_sup > rango_inf >= 0:
            fecha, consumo = self.procesar(rango_inf, rango_sup)    # Proceso el archivo entre los dias dados
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
            data.close()    # cierro el archivo
            print("se escribio el archivo  con los datos respectivos")


if __name__ == '__main__':
    file = Archivo("MC-SIN-OFI-DR-Septiembre-2020.csv", "./")
    print(file)
    print(type(file))
    print(file.maxconsumo)
    dos, uno = file.procesar(5, 8)
    file.escribr("hola.txt", False, fecha=dos,consumo=uno)
