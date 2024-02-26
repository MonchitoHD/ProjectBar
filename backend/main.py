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
        print("Felicidades la conexion a sido exitosa")
    except Exception as e:
        print(e)

    #Una vez se hace la conexion se crean las mesas    
    mesas = database.mesas
    mesas.delete_many({})
    array_mesas = [
        {"numero_mesa":1,"tipo": "mesa", "asientos":2, "estado":"ocupada"},
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


#Menu para gestionar el funcionamiento de la aplicacion de terminal
def mostrar_menu():
    print("-------Menu--------")
    print("1. Ver Mesas")
    print("2. Reservar mesas")
    print("3. Gestionar pedidos")
    print("4. Liberar mesas")
    print("5. Ver factura")

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
    mesas = database.mesas.find()
    mesas_barra = database.barra.find()
    mesas_terraza = database.terraza.find()
    numero_mesas = [mesa["numero_mesa"] for mesa in mesas]
    numero_mesas_barra = [mesa["numero_mesa"] for mesa in mesas_barra]
    numero_mesas_terraza = [mesa["numero_mesa"] for mesa in mesas_terraza]
    estado_mesas = [mesa["estado"] for mesa in mesas]
    estado_mesas_barra = [mesa["estado"] for mesa in mesas_barra]
    estado_mesas_terraza = [mesa["estado"] for mesa in mesas_terraza]
    numero_mesa = int(input("Introduce el número de la mesa de la que quieras el QR: "))
    if (numero_mesa in numero_mesas and estado_mesas[numero_mesas.index(numero_mesa)] == "ocupada") or \
       (numero_mesa in numero_mesas_barra and estado_mesas_barra[numero_mesas_barra.index(numero_mesa)] == "ocupada") or \
       (numero_mesa in numero_mesas_terraza and estado_mesas_terraza[numero_mesas_terraza.index(numero_mesa)] == "ocupada"):
        generar_qr(numero_mesa)
    else:
        print("El número de mesa no coincide o el estado de la mesa no es ocupada. Por favor, revise los datos introducidos.")



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
    print("Hola mundo")

def opcion3():
    print("Hola mundo")

def opcion4():
    print("Hola mundo")

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

