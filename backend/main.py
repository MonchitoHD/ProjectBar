from pymongo.mongo_client import MongoClient

import qrcode

database = None
def conectar_mongodb():
    global database
    uri = "mongodb+srv://Hugitoo:666@cluster0.zoc9ooy.mongodb.net/?retryWrites=true&w=majority"

    client = MongoClient(uri)
    database = client.bar
    try:
        client.admin.command('ping')
        print("Felicidades la conexion ha sido exitosa")
    except Exception as e:
        print(e)

    #Una vez se hace la conexion se crean las mesas    
    mesas = database.mesas
    mesas.delete_many({})
    array_mesas = [
        {"numero_mesa":1,"tipo": "mesa", "asientos":2, "estado":"libre"},
        {"numero_mesa":2,"tipo": "mesa", "asientos":3, "estado":"libre"},
        {"numero_mesa":3,"tipo": "mesa", "asientos":4, "estado":"libre"},
        {"numero_mesa":4,"tipo": "mesa", "asientos":5, "estado":"libre"},
        {"numero_mesa":5,"tipo": "mesa", "asientos":6, "estado":"libre"}
    ]
    mesas.insert_many(array_mesas)

    #Una vez se realiza la conexion se crea la barra
    barra = database.barra
    barra.delete_many({})
    barra_data = {"numero_mesa":6,"tipo": "barra", "asientos":5, "estado":"libre"}
    barra.insert_one(barra_data)

    #Una vez se realiza la conexion se crean las mesas de la terraza
    terraza = database.terraza
    terraza.delete_many({})
    mesas_terraza = [
        {"numero_mesa":7,"tipo": "terraza", "asientos":2, "estado":"libre"},
        {"numero_mesa":8,"tipo": "terraza", "asientos":4, "estado":"libre"},
        {"numero_mesa":8,"tipo": "terraza", "asientos":6, "estado":"libre"}
    ]
    terraza.insert_many(mesas_terraza)

    #Una vez se establece la conexion se crea la carta con las diferentes opciones a disposicion
    carta = database.carta
    carta.delete_many({})
    elementos_carta = [
        {"nombre": "Plato individual","precio":10},
        {"nombre": "Menu del dia", "precio":20},
        {"nombre": "Bebidas", "precio":6}
    ]
    carta.insert_many(elementos_carta)


    return database

if __name__ == "__main__": 
    conectar_mongodb()

#Funcion que muestra todas las mesas que hay en la BD con todos sus datos
def mostrar_mesas():
    global database
    mesas = database.mesas.find()
    mesas_barra = database.barra.find()
    mesas_terraza = database.terraza.find()
    for mesa in mesas:
        print(mesa)
    for mesa in mesas_barra:
        print(mesa)    
    for mesa in mesas_terraza:
        print(mesa)

#Funcion que genera un QR para la mesas seleccionada
def generar_qr(numero_mesa): 
        enlace_expo = f'exp://exp.host/projectbar/mesa/{numero_mesa}'
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(enlace_expo)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.show()

#Funcion que muestra el QR genrado con la funcion generar_qr si el numero de la mesa coincide y su estado es ocupada
def ver_qr():
       global database
       mesas_tipos = [("mesas", database.mesas), ("barra", database.barra), ("terraza", database.terraza)]
       numero_seleccionado = input("Introduce el número de la mesa de la que quieras el QR: ")
       mesa_encontrada = False
       for tipo, collection in mesas_tipos:
        print(f"Mesas tipo {tipo}:")
        for mesa in collection.find():
            numero_mesa = mesa["numero_mesa"]
            estado_mesa = mesa["estado"]
            print(f"Número de mesa: {numero_mesa}, Estado: {estado_mesa}")

            if numero_seleccionado == str(numero_mesa) and estado_mesa == "ocupada":
                generar_qr(numero_seleccionado)
                mesa_encontrada = True
                break
            
        if not mesa_encontrada:
            print("Revisa los datos: la mesa debe existir y estar ocupada.")

#Funcion para reservar mesas, preguntara cuntos clientes vienen buscara una mesa con la misma cantidad de asientos y le cambiara a estado de ocupada
def reservar_mesa():
    global database
    mesas_restaurante = [("mesas", database.mesas), ("barra", database.barra), ("terraza", database.terraza)]
    numero_clientes = input("Diganme cuantos vais a ser: ")
    mesa_encontrada = False
    for collection_nombre, collection in mesas_restaurante:
        for mesa in collection.find():
            asientos_mesa = mesa["asientos"]
            estado_mesa = mesa["estado"]
            if numero_clientes == str(asientos_mesa) and estado_mesa == "libre":
                print("Te hemos encontrado una mesa. Gracias por llamar.")
                collection.update_one({"_id": mesa["_id"]}, {"$set": {"estado": "ocupada"}})
                mesa_encontrada = True
                break
        if mesa_encontrada:
            break
    if not mesa_encontrada:
        print("Lo sentimos no nos quedan mesas libres.")        

#Funcion para liberar una mesa es decir cambia el estado de la mesa seleccionada de ocupada a libre
def liberar_mesa():
    global database
    mesas_restaurante = [("mesas", database.mesas), ("barra", database.barra), ("terraza", database.terraza)]
    mesa_a_liberar = input("Oiches meu dime que mesa hay que liberar: ")
    for collection_nombre, collection in mesas_restaurante:
        for mesa in collection.find():
            numero_mesa = mesa["numero_mesa"]
            estado_mesa = mesa["estado"]
            if mesa_a_liberar == str(numero_mesa) and estado_mesa == "ocupada":
                print("Valee jefe ya la ví la libero ahora")
                collection.update_one({"_id" : mesa["_id"]}, {"$set": {"estado":"libre"}})
                print("Jefee la mesa ya esta liberada")
                break
            else:
                print("Jefeee solo mentir he!! La mesa ya esta libre")    


#Menu para gestionar el funcionamiento de la aplicacion de terminal
def mostrar_menu():
    print("-------Menu--------")
    print("1. Ver Mesas")
    print("2. Reservar mesas")
    print("3. Gestionar pedidos")
    print("4. Liberar mesas")
    print("5. Ver factura")

#Menu para gestionar las mesas 
def menu_mesas():
    print("Opciones Mesas")
    print("1. Ver Mesas")
    print("2. Ver QR")

def opcion1_mesas():
    mostrar_mesas()

def opcion2_mesas():
    ver_qr()

def gestion_mesas():
    menu_mesas()
    opcion = input("Seleccione una opcion: ")

    if opcion == "1":
        opcion1_mesas()
    elif opcion == "2":
        opcion2_mesas()


#Opciones del menu principal
def opcion1():
    gestion_mesas()

def opcion2():
    reservar_mesa()

def opcion3():
    print("Hola mundo")

def opcion4():
    liberar_mesa()

def opcion5():
    print("Hola mundo")

while True:
    mostrar_menu()
    opcion = input("Seleccione una opcion: ")

    if opcion == "1":
        opcion1()
    elif opcion == "2":
        opcion2()
    elif opcion == "3":
        opcion3()
    elif opcion == "4":
        opcion4()
    elif opcion == "5":
        opcion5()
    else:
        print("La opcion que has seleccionado es incorrecta.")    

