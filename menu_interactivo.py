"""
Menú para elegir lo que quieres realizar con respecto al cliente
"""

# Importamos módulos propios
from modelos import Cliente
from repositorio import RepositorioClientes

# Importamos módulos
from datetime import date, datetime

# ---Funciones para el menú
def cabecera(titulo):
    '''Crea la misma cabecera para cada opción del menú'''
    print()
    print("=" * len(titulo))
    print(f"{titulo.upper()}")
    print("=" * len(titulo))

def crear_cliente(repositorio):
    '''Crea un cliente y lo guarda en el repositorio'''
    cabecera("crear cliente")
    id_cliente = input("ID del cliente: ")
    nombre = input("Nombre: ")
    while True:
        fecha_nacimiento = input("Fecha de nacimiento (DD/MM/AAAA): ")
        try:
            nuevo_cliente = Cliente(
                id_cliente, nombre, fecha_nacimiento
                )  # deja de ser None
            repositorio.guardar(nuevo_cliente)  # se guarda en disco al momento
            print(f"Cliente '{nombre}' creado y guardado con ID '{id_cliente}'.")
            return nuevo_cliente # devuelve el cliente que se ha creado
    
        except ValueError as e:
            print(e)  # muestra el mensaje del raise

def cargar_cliente(repositorio):
    '''Carga la información del cliente solicitado'''
    cabecera("cargar cliente")
    id_cliente = input("Introduce el ID del cliente: ")
    try:
        cliente = repositorio.cargar(id_cliente)
        print(f"Cliente '{cliente.nombre}' con ID '{id_cliente}' cargado correctamente.")
        return cliente
    except FileNotFoundError:
        print(f"No se ha encontrado ningún cliente con el ID {id_cliente}.")
        return None #devuelve None si no encuentra el ID del cliente

def ver_citas(cliente_activo):
    '''Muestra las citas del cliente'''
    cabecera("citas del cliente")
    if cliente_activo.citas:
        for numero, cita in enumerate(cliente_activo.citas, start=1):
            print(
                f"{numero}: {cita.fecha_cita.strftime('%d/%m/%Y')} - {cita.anotacion}"
                )
    else:
        print(f"El cliente '{cliente_activo.nombre}' no tiene citas registradas.")

def ver_dolencias(cliente_activo):
    '''Muestra las dolencias del cliente y el estado'''
    cabecera("dolencias del cliente")
    if cliente_activo.dolencias:
        for numero, d in enumerate(cliente_activo.dolencias, start=1):
            print(f"{numero}: {d.descripcion} ({d.estado}) - inicio {d.inicio.strftime('%d/%m/%Y')}"
                  )
            for obs in d.observaciones:
                print(f"     -{obs['fecha']} - {obs['texto']} ")
        return True
    
    else:
        print(f"El cliente {cliente_activo.nombre} no tiene dolencias asociadas.")
        return False

def agregar_cita(cliente_activo, repositorio):
    '''Añade una nueva cita al cliente'''
    cabecera("agregar cita")
    anotacion = input("Nota sobre la cita: ")
    while True:
        fecha = input("Introduce el día de la nueva cita(DD/MM/AAAA): ")
        try:
            cliente_activo.agregar_cita(fecha, anotacion)
            repositorio.guardar(cliente_activo)
            break
        except ValueError as e:
            print(e)  # muestra el mensaje del raise

def agregar_dolencia(cliente_activo, repositorio):
    '''Añade una dolencia al cliente'''
    cabecera("agregar dolencia")
    descripcion = input("Introduce la dolencia del cliente: ")
    while True:
        inicio = input("Introduce el día aproximado que empezó la dolencia(DD/MM/AAAA): ")
        try:
            cliente_activo.agregar_dolencia(descripcion, inicio)
            repositorio.guardar(cliente_activo)
            print(f"Dolencia añadida a '{cliente_activo.nombre}' correctamente.")
            break

        except ValueError as e:
            print(e)  # muestra el mensaje del raise

def resolver_dolencia(cliente_activo, repositorio):
    '''Marca en estado resuelta una dolencia'''
    if not ver_dolencias(cliente_activo): # Si el cliente no tiene dolencias(False)
        return
    try:
        numero = int(input("Introduce el número de dolencia que quieres marcar como resuelta: "))
        resultado = cliente_activo.resolver_dolencia(numero) # Si devuelve True
        if resultado == "resuelta":
            repositorio.guardar(cliente_activo)
            print("La dolencia se ha resuelto correctamente.")
        elif resultado == "ya resuelta":
            print("La dolencia ya estaba anteriormente resuelta.")
        else:
            print("No se ha encontrado la dolencia")
    except ValueError:
        print("Por favor, introduce un número.")

cliente_activo = None  # ← se crea una vez, fuera del bucle (variable de estado)
repositorio = RepositorioClientes("clientes")  # creamos el repositorio por defecto

while True:
    print("\n------ MENÚ ------")
    print("1. Crear cliente")
    print("2. Cargar cliente")
    print("3. Agregar cita")
    print("4. Ver todas las citas")
    print("5. Agregar dolencia")
    print("6. Resolver dolencia")
    print("7. Agregar observación")
    print("8. Resumen del cliente")
    print("9. Listar clientes")
    print("10. Salir del programa")
    opcion = input("Introduce la opción que deseas elegir: ")

    # Verificamos que haya cliente para las opciones 3 al 8
    if opcion in ["3", "4", "5", "6", "7", "8"] and cliente_activo is None:
        print("Necesitas crear o cargar un cliente antes de elegir esta opción.")
        continue

    if opcion == "1":
        cliente_activo = crear_cliente(repositorio)

    elif opcion == "2":
        resultado = cargar_cliente(repositorio)
        if resultado is not None:
            cliente_activo = resultado
        # Si devuelve None no se modifica nada y sigue manteniendo el cliente activo anterior

    elif opcion == "3":
        agregar_cita(cliente_activo, repositorio)

    elif opcion == "4":
        ver_citas(cliente_activo)

    elif opcion == "5":
        agregar_dolencia(cliente_activo, repositorio)

    elif opcion == "6":
        resolver_dolencia(cliente_activo, repositorio)

    elif opcion == "7":
        if not ver_dolencias(cliente_activo): # Si el cliente no tiene dolencias(False)
            continue

        texto = input("Introduce la observación: ")
        while True:
            try:
                numero = int(input("Introduce el número de la dolencia: "))
                if cliente_activo.agregar_observacion_a_dolencia(
                    numero, texto
                ):  # Si devuelve True
                    repositorio.guardar(cliente_activo)
                    break
            except ValueError:
                print("Por favor, introduce un número.")

    elif opcion == "8":
        cliente_activo.mostrar_info()
        ver_dolencias(cliente_activo)

    elif opcion == "9":
        clientes = repositorio.listar_clientes()
        if clientes:
            for c in clientes:
                print(f"ID: {c['id_cliente']} / Nombre: {c['nombre']}")
        else:
            print("Aún no hay clientes registrados.")

    elif opcion == "10":
        print("\nSaliendo del programa...")
        break

    else:
        print("\nPor favor, introduce una opción válida.")



if __name__ == "__main__":
    cabecera = cabecera("Crear cliente")