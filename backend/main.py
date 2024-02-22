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
        {"tipo": "mesa", "asientos":2, "estado":"libre"},
        {"tipo": "mesa", "asientos":3, "estado":"libre"},
        {"tipo": "mesa", "asientos":4, "estado":"libre"},
        {"tipo": "mesa", "asientos":5, "estado":"libre"},
        {"tipo": "mesa", "asientos":6, "estado":"libre"}
    ]
    mesas.insert_many(array_mesas)

    #Una vez se realiza la conexion se crea la barra
    barra = database.barra
    barra.delete_many({})
    barra_data = {"tipo": "barra", "asientos":5, "estado":"libre"}
    barra.insert_one(barra_data)

    #Una vez se realiza la conexion se crean las mesas de la terraza
    terraza = database.terraza
    terraza.delete_many({})
    mesas_terraza = [
        {"tipo": "terraza", "asientos":2, "estado":"libre"},
        {"tipo": "terraza", "asientos":4, "estado":"libre"},
        {"tipo": "terraza", "asientos":6, "estado":"libre"}
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