# Importamos módulos propios
from modelos import Cliente, Cita, Dolencia

# Importamos módulos
import json
from pathlib import Path
import sqlite3


class RepositorioClientes:
    def __init__(self, carpeta="."):  # carpeta actual
        self.carpeta = carpeta
        Path(self.carpeta).mkdir(exist_ok=True)  # crea la carpeta si no existe
        ruta_bd = Path(self.carpeta) / "clientes.db"
        #Construir la ruta y conectar
        self.conexion = sqlite3.connect(ruta_bd)
        self.conexion.execute('PRAGMA foreign_keys = ON')
        self.conexion.executescript("""
            CREATE TABLE IF NOT EXISTS clientes(
	            id INTEGER PRIMARY KEY,
	            nombre TEXT NOT NULL,
	            nacimiento TEXT)
            ;

            CREATE TABLE IF NOT EXISTS dolencias(
                id INTEGER PRIMARY KEY,
                cliente_id INTEGER NOT NULL,
                descripcion TEXT,
                inicio TEXT,
                estado TEXT,
                resolucion TEXT,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id)
            );

            CREATE TABLE IF NOT EXISTS citas(
                id INTEGER PRIMARY KEY,
                cliente_id INTEGER NOT NULL,
                fecha_cita TEXT NOT NULL,
                anotacion TEXT,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id)
            );

            CREATE TABLE IF NOT EXISTS observaciones(
                id INTEGER PRIMARY KEY,
                dolencia_id INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                texto TEXT,
                FOREIGN KEY (dolencia_id) REFERENCES dolencias(id)
            );
                    
            """)

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

        cliente_id = self.conexion.execute("INSERT INTO clientes(nombre, nacimiento) VALUES (?, ?)",
                              (cliente.nombre, cliente.nacimiento.strftime("%Y-%m-%d"))).lastrowid
        #lastrowid --> Devuelve el id que se ha creado automáticamente

        for dolencia in cliente.dolencias:
            dolencia_id = self.conexion.execute("INSERT INTO dolencias(cliente_id, descripcion, inicio, estado, resolucion) VALUES (?,?,?,?,?)",
            (cliente_id, dolencia.descripcion, dolencia.inicio.strftime("%Y-%m-%d"), dolencia.estado, dolencia.resolucion)).lastrowid
            for obs in dolencia.observaciones:
                self.conexion.execute("INSERT INTO observaciones(dolencia_id, fecha, texto) VALUES (?,?,?)",
                                      (dolencia_id, obs["fecha"], obs["texto"]))
        
        for cita in cliente.citas:
            self.conexion.execute("INSERT INTO citas(cliente_id, fecha_cita, anotacion) VALUES (?, ?, ?)",
                                  (cliente_id, cita.fecha_cita.strftime("%Y-%m-%d"), cita.anotacion))

        
        self.conexion.commit()

    def cargar(self, id_cliente):
        """Carga un cliente desde el JSON y reconstruye el objeto"""
        nombre_archivo = f"{self.carpeta}/Cliente_{id_cliente}.json"
        try:
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

        except (
            FileNotFoundError,
            TypeError,
            ValueError,
            KeyError,
            json.JSONDecodeError,
        ):
            # El archivo no existe o está dañado
            return None

    # NOTA: este método recorre los archivos JSON para listar a los clientes.
    # Es válido para pocos registros pero a una mayor escala es ineficiente abrir cada archivo
    # en cada consulta, tendríamos que migrar los archivos JSON a una base de datos
    # (SQLite, por ejemplo) donde haríamos una consulta directa sin recorrer archivos.
    def listar_clientes(self):
        """Devuelve una lista de dict con id y nombre del cliente"""
        clientes = []
        # .glob para buscar archivos con el patrón "Cliente_*.json"
        for archivo in Path(self.carpeta).glob("Cliente_*.json"):
            try:
                with open(archivo, "r", encoding="utf-8") as file:
                    datos = json.load(file)
                clientes.append(
                    {
                        "id_cliente": datos["id_cliente"],
                        "nombre": datos["nombre"],
                    }
                )
            except (json.JSONDecodeError, TypeError, ValueError, KeyError):
                continue
        return clientes

    def existe_cliente(self, id_cliente):
        """Devuelve True si ya hay un cliente con dicho ID"""
        nombre_archivo = f"{self.carpeta}/Cliente_{id_cliente}.json"
        return Path(nombre_archivo).exists()  # ¿hay un archivo real en esa ruta?


