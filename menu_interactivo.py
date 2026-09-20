'''
Menú para elegir lo que quieres realizar con respecto al cliente
'''

# Importamos módulos propios
from clases_clientes import Cliente
from repositorio import RepositorioClientes
# Importamos módulos
from datetime import date, datetime


cliente_activo = None   # ← se crea una vez, fuera del bucle (variable de estado)
repositorio = RepositorioClientes() # creamos el repositorio por defecto

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
        print("\n--- Crear cliente ---")
        id_cliente = input("ID del cliente: ")
        nombre = input("Nombre: ")
        while True:
            fecha_nacimiento = input("Fecha de nacimiento (DD/MM/AAAA): ")
            try:
                cliente_activo = Cliente(id_cliente, nombre, fecha_nacimiento) # deja de ser None
                repositorio.guardar(cliente_activo)   # se guarda en disco al momento
                print(f"Cliente '{nombre}' creado y guardado con ID {id_cliente}.")
                break

            except ValueError as e:
                print(e) #muestra el mensaje del raise
        
    elif opcion == "2":
        print("\n--- Cargar cliente ---")
        id_cliente = input("Introduce el ID del cliente: ")
        try:
            cliente_activo = repositorio.cargar(id_cliente)
            print(cliente_activo)
        except FileNotFoundError:
            print(f"El ID {id_cliente} no existe.")

    elif opcion == "3":
        print("\n--- Agregar cita ---")
        anotacion = input("Nota sobre la cita: ")
        while True:
            fecha = input("Introduce el día de la nueva cita(DD/MM/AAAA): ")
            try:
                cliente_activo.agregar_cita(fecha, anotacion)
                repositorio.guardar(cliente_activo)
                break
            except ValueError as e:
                print(e) #muestra el mensaje del raise
            
    elif opcion == "4":
        print("\n--- Citas del cliente ---")
        cliente_activo.ver_citas()

    elif opcion == "5":
        print("\n--- Agregar dolencia ---")
        descripcion = input("Introduce la dolencia del cliente: ")
        while True:
            inicio = input("Introduce cuando comenzó la dolencia(DD/MM/AAAA): ")
            try:
                cliente_activo.agregar_dolencia(descripcion, inicio)
                repositorio.guardar(cliente_activo)
                break
            except ValueError as e:
                print(e) #muestra el mensaje del raise

    elif opcion == "6":
        print("\n--- Resolver dolencia ---")
        cliente_activo.ver_dolencias()
        try:
            numero = int(input("Introduce el número de dolencia que quieres marcar como resuelta: "))
            cliente_activo.resolver_dolencia(numero)
            repositorio.guardar(cliente_activo)
        except ValueError:
            print("Por favor, introduce un número.")

    elif opcion == "7":
        print("\n--- Agregar observación ---")
        cliente_activo.ver_dolencias()
        
        texto = input("Introduce la observación: ")
        while True:
            try:
                numero = int(input("Introduce el número de la dolencia: "))
                if cliente_activo.agregar_observacion_a_dolencia(numero, texto): # Si devuelve True
                    repositorio.guardar(cliente_activo)
                    break
            except ValueError:
                print("Por favor, introduce un número.")

    elif opcion == "8":
        print("\n--- Resumen del cliente ---")
        cliente_activo.mostrar_info()
        cliente_activo.ver_dolencias()

    elif opcion == "9":
        print("\n --- Lista de clientes ---")
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