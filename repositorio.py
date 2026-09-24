# Importamos módulos propios
from modelos import Cliente, Cita, Dolencia

# Importamos módulos
import json
from pathlib import Path


class RepositorioClientes:
    def __init__(self, carpeta="."):  # carpeta actual
        self.carpeta = carpeta
        Path(self.carpeta).mkdir(exist_ok=True) # crea la carpeta si no existe

    def guardar(self, cliente: Cliente):
        """Guarda los datos del cliente en un archivo JSON"""
        datos = {
            "id_cliente": cliente.id_cliente,
            "nombre": cliente.nombre,
            # nacimiento lo convertimos a str para poder guardarlo en json
            "nacimiento": cliente.nacimiento.strftime("%d/%m/%Y"),
            # Serialización de Dolencias y Citas
            "dolencias": [dolencia.a_diccionario() for dolencia in cliente.dolencias],
            "citas": [cita.a_diccionario() for cita in cliente.citas],
        }

        nombre_archivo = f"{self.carpeta}/Cliente_{cliente.id_cliente}.json"
        with open(nombre_archivo, "w", encoding="utf-8") as file:
            json.dump(datos, file, ensure_ascii=False, indent=4)

    def cargar(self, id_cliente):
        """Carga un cliente desde el JSON y reconstruye el objeto"""
        nombre_archivo = f"{self.carpeta}/Cliente_{id_cliente}.json"
        with open(nombre_archivo, "r", encoding="utf-8") as file:
            datos = json.load(file)  # json.load devuelve un diccionario

        # creamos el objeto Cliente con los valores sacados del dict 'datos'
        cliente = Cliente(
            id_cliente=datos["id_cliente"],
            nombre=datos["nombre"],
            nacimiento=datos["nacimiento"],
            # Desserialización de Dolencias y Citas
            dolencias=[Dolencia.a_objeto(dic) for dic in datos["dolencias"]],
            citas=[Cita.a_objeto(dic) for dic in datos["citas"]],
        )

        return cliente

    # NOTA: este método recorre los archivos JSON para listar a los clientes.
    # Es válido para pocos registros pero a una mayor escala es ineficiente abrir cada archivo
    # en cada consulta, tendríamos que migrar los archivos JSON a una base de datos
    # (SQLite, por ejemplo) donde haríamos una consulta directa sin recorrer archivos.
    def listar_clientes(self):
        """Devuelve una lista de dict con id y nombre del cliente"""
        clientes = []
        # .glob para buscar archivos con el patrón "Cliente_*.json"
        for archivo in Path(self.carpeta).glob("Cliente_*.json"):
            with open(archivo, "r", encoding="utf-8") as file:
                datos = json.load(file)
            clientes.append(
                {
                    "id_cliente": datos["id_cliente"],
                    "nombre": datos["nombre"],
                }
            )
        return clientes

    def existe_cliente(self, id_cliente):
        '''Devuelve True si ya hay un cliente con dicho ID'''
        nombre_archivo = f"{self.carpeta}/Cliente_{id_cliente}.json"
        return Path(nombre_archivo).exists() # ¿hay un archivo real en esa ruta?