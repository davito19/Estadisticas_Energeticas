import os
import datetime as dt


class Archivo():
    def __init__(self, name, base_dir):
        self.name = name
        self.base_dir = base_dir
        self.path = os.path.join(base_dir, name)

    def __str__(self):
        assert  isinstance(self, Archivo), "El atributo debe ser tipo Archivo"
        return "Archivo: {} Ruta: {}".format(self.name, self.base_dir)

    def MaxConsumo(self):
        file = open(self.path)
        enc = file.readline()
        enc = enc.split(";")

        demanda = []
        fechas = []
        fecha_m = 0
        mayor = 0

        for datos in file:
            datos = datos.split(";")

            fecha = datos[2]

            demanda_dia = datos[4:28]
            horas = []

            for i in range(len(demanda_dia)):
                demanda_dia[i] = float((demanda_dia[i].replace(",", ".")))
                horas.append(dt.datetime.strptime(fecha + " " + str(i), "%Y-%m-%d %H"))

            demanda.extend(demanda_dia)
            fechas.extend(horas)

        for i in range(len(demanda)):
            if demanda[i] >= mayor:  # determina el nuevo valor de mayor consumo
                fecha_m = fechas[i]  # guarda el mayor consumo
                mayor = demanda[i]  # guarda la fecha de mayor consumo

        file.close()
        #print("La demanda máxima se dio el {} y fue de {}W".format(fecha_m, mayor))
        return echa_m, mayor



if __name__ == '__main__':
    file = Archivo("MC-SIN-OFI-DR-Septiembre-2020.csv", "./")
    print(file)
    print(type(file))
    print(file.MaxConsumo())


