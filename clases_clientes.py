'''clases Cliente, Cita, Dolencia'''
# importamos módulos
from datetime import date, datetime


class Cita:
    def __init__(self, fecha_cita, anotacion):
        self.fecha_cita = datetime.strptime(fecha_cita, "%d/%m/%Y").date()
        self.anotacion = anotacion

    def __repr__(self):
        return (f"Día ({self.fecha_cita}: '{self.anotacion}')")

    def a_diccionario(self):
        '''Convierte el objeto Cita a dict para guardar en JSON'''
        return {
            'fecha': self.fecha_cita.strftime("%d/%m/%Y"),
            'anotacion': self.anotacion
            }

    @classmethod
    def a_objeto(cls, dic):
        '''Crea una clase Cita a partir del diccionario'''
        return cls(dic['fecha'], dic['anotacion'])


class Dolencia:
    def __init__(self, descripcion, inicio, estado='Activa', resolucion=None, observaciones=None):
        self.descripcion = descripcion
        self.inicio = datetime.strptime(inicio, "%d/%m/%Y").date()
        self.estado = estado
        self.resolucion = resolucion
        self.observaciones = observaciones if observaciones is None else []

    def __repr__(self):
        return f"Dolencia {self.descripcion} - {self.estado}"

    def a_diccionario(self):
            '''Convierte el objeto Dolencia a dict para guardar en JSON'''
            return {
                'descripcion': self.descripcion,
                'inicio': self.inicio.strftime("%d/%m/%Y"),
                'estado': self.estado,
                'resolucion': self.resolucion,
                'observaciones': self.observaciones
                }

    @classmethod
    def a_objeto(cls, dic):
        '''Crea una clase Dolencia a partir del diccionario'''
        return cls(dic['descripcion'], dic['inicio'], dic['estado'], dic['resolucion'], dic['observaciones'])


    def agregar_observacion(self, texto):
        '''Añade observación y fecha a una dolencia'''
        observacion = {
            "fecha": date.today().strftime("%d/%m/%Y"),
            "texto": texto, 
        }
        self.observaciones.append(observacion)
        print("Observación agregada correctamente.")



class Cliente:
    def __init__(self, id_cliente, nombre, nacimiento, dolencias=None, citas=None):
        self.id_cliente = id_cliente
        self.nombre = nombre.title()
        self.nacimiento = datetime.strptime(nacimiento, "%d/%m/%Y").date()
        self.dolencias = dolencias if dolencias is not None else []
        self.citas = citas if citas is not None else []

    def __repr__(self):
        return (f"Cliente {self.id_cliente}: {self.nombre}")

    def mostrar_info(self):
        '''Muestra toda la informacion del cliente'''
        print(f"\nINFORMACIÓN CLIENTE {self.nombre.upper()}")
        print(f"ID: {self.id_cliente}")
        print(f"Nombre: {self.nombre}")
        print(f"Nacimiento: {self.nacimiento.strftime('%d/%m/%Y')} ({self.edad} años)")
        print(f"Dolencias registradas: {len(self.dolencias)}")
        print(f"Total citas: {len(self.citas)}")

    @property
    def edad(self):
        '''Calcula la edad del cliente'''
        hoy = date.today()
        edad = hoy.year - self.nacimiento.year
        if (hoy.month, hoy.day) < (self.nacimiento.month, self.nacimiento.day):
            edad -= 1
        return edad

    def agregar_dolencia(self, descripcion, inicio):
        '''Añade nueva dolencia'''
        nueva_dolencia = Dolencia(descripcion, inicio)
        self.dolencias.append(nueva_dolencia)
        print("Dolencia agregada correctamente.")

    def resolver_dolencia(self, numero):
        '''Cambia el estado de la dolencia activa/resuelta.'''
        indice = numero - 1
        if 0 <= indice < len(self.dolencias):
            dolencia = self.dolencias[indice]
            dolencia.estado = "Resuelta"
            dolencia.resolucion = date.today().strftime("%d/%m/%Y")
            print(f"La dolencia {dolencia.descripcion} se ha guardado como resuelta.")
        else:
            print("No se ha encontrado el número de la dolencia.")

    def ver_dolencias(self):
        '''Muestra las dolencias del cliente y el estado'''
        print("\n--- Dolencias del cliente ---")
        if self.dolencias:
            for numero, d in enumerate(self.dolencias, start=1):
                print(f"{numero} - {d.descripcion} ({d.estado}) - inicio {d.inicio.strftime('%d/%m/%Y')}")
        else:
            print("No hay dolencias registradas.")
        
    def agregar_cita(self, fecha_cita, anotacion):
        '''Añade cita al cliente'''
        nueva_cita = Cita(fecha_cita, anotacion)
        self.citas.append(nueva_cita)
        print(f"Cita del día '{fecha_cita}' agregada correctamente.")

    def ver_citas(self):
        '''Muestra las fechas y anotaciones de las citas'''
        print("\n--- Citas del cliente ---")
        if self.citas:
            for numero, cita in enumerate(self.citas, start=1):
                print(f"{numero}: {cita.fecha_cita.strftime('%d/%m/%Y')} - {cita.anotacion}")
        else:
            print("No hay citas registradas.")

    

# ejemplo de uso
if __name__ == "__main__":
    cliente = Cliente("123", "juana rivas", "20/03/1988", ["tendinitis hombro"])
    #cliente.mostrar_info()
    #cliente.agregar_dolencia('otitis')
    #cliente.mostrar_info()
    #cliente.eliminar_dolencia("tendinitis hombro")
    #cliente.agregar_cita('04/05/2026')
    #cliente.agregar_cita('25/06/2026')
    #cliente.agregar_cita('03/07/2026')
    #cliente.mostrar_info()
    #ultima_cita = cliente.ultima_cita()
    #print(ultima_cita)
    #todas_citas = cliente.total_citas()
    #print(todas_citas)
    #cliente.agregar_observacion("Hombro totalmente recuperado.")
    #cliente_cargado = Cliente.cargar_json("123")
    #cliente_cargado.mostrar_info()
    #cliente.resumen_clinico()
    #cita = Cita("17/08/2026", "Trabajamos hombro")
    #print(cita)
    #cliente.agregar_cita("17/08/2026", "Trabajamos hombro")
    #cliente_cargado = Cliente.cargar_json("123")
    #print(cliente_cargado.citas)
    #print(cliente_cargado.citas[0].anotacion)
    dolencia = Dolencia("Tortícolis lado derecho del cuello", "20/08/2026")
    print(dolencia)
    dic = dolencia.a_diccionario()
    print(dic)
    dic_2 = dolencia.a_objeto(dic)
    print(dic_2)
    print(dic_2.inicio)