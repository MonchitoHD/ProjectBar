from pymongo.mongo_client import MongoClient

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
    print("Hola Mundo") 

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

