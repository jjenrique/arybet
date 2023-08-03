from .entities.User import User


class ModelUser():

    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, username, password, fullname FROM user 
                    WHERE username = '{}'""".format(user.username)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = User(row[0], row[1], User.check_password(
                    row[2], user.password), row[3])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, username, fullname FROM user WHERE id = {}".format(
                id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(row[0], row[1], None, row[2])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)


class Cliente:
    def __init__(self, razon_social, rut, telefono, email, persona_de_contacto):
        self.razon_social = razon_social
        self.rut = rut
        self.telefono = telefono
        self.email = email
        self.persona_de_contacto = persona_de_contacto

    @classmethod
    def obtener_todos(self, mysql, offset, limit):
        connection = mysql.connection
        cursor = connection.cursor()
        cursor.execute("SELECT razon_social, rut, telefono, email, persona_de_contacto FROM clientes ORDER BY id DESC LIMIT %s OFFSET %s", (limit, offset))
        resultados = cursor.fetchall()
        cursor.close()

        clientes = []
        for resultado in resultados:
            cliente = self(resultado[0], resultado[1], resultado[2], resultado[3], resultado[4])
            clientes.append(cliente)

        return clientes
    
    def insertar(self, mysql):
        connection = mysql.connection
        cursor = connection.cursor()
        cursor.execute("INSERT INTO clientes (razon_social, rut, telefono, email, persona_de_contacto) VALUES (%s, %s, %s, %s, %s)",
                       (self.razon_social, self.rut, self.telefono, self.email, self.persona_de_contacto))
        connection.commit()
        cursor.close()

class Cotizacion:
    def __init__(self, id, fecha, fecha_entrega, cliente_id):
        self.id = id
        self.fecha = fecha
        self.fecha_entrega = fecha_entrega
        self.cliente_id = cliente_id

    @classmethod
    def obtener_todos(cls, mysql, offset, limit):
        connection = mysql.connection
        cursor = connection.cursor()
        cursor.execute("SELECT id, fecha, fecha_entrega, cliente_id FROM cotizaciones ORDER BY id ASC LIMIT %s OFFSET %s", (limit, offset))
        resultados = cursor.fetchall()
        cursor.close()

        cotizaciones = []
        for resultado in resultados:
            cotizacion = cls(resultado[0], resultado[1], resultado[2], resultado[3])
            cotizaciones.append(cotizacion)

        return cotizaciones
