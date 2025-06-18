from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getYears():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct(year(s.`datetime`)) as year
                        from new_ufo_sightings.sighting s  """
            cursor.execute(query)

            for row in cursor:
                result.append(row["year"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getStatesOfYear(year):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct(s2.id) as id, s2.Name 
                        from new_ufo_sightings.sighting s, new_ufo_sightings.state s2 
                        where year(s.`datetime`) = %s and s.state = s2.id 
                        order by s2.Name   """
            cursor.execute(query, (year, ))

            for row in cursor:
                result.append(row["id"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getNodes(year, state):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select *
                        from new_ufo_sightings.sighting s
                        where  year(s.`datetime`)= %s  and s.state = %s"""
            cursor.execute(query, (year, state))

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getEdges(year, state):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s.id as one, s2.id as two
                        from new_ufo_sightings.sighting s, new_ufo_sightings.sighting s2
                        where   s.state = s2.state
                                and s.id <> s2.id
                                and year(s.`datetime`) = year(s2.`datetime`)
                                and s.shape = s2.shape
                                and s.id > s2.id
                                and year(s.`datetime`)= %s
                                and s.state = %s 
                                 """
            cursor.execute(query, (year, state))

            for row in cursor:
                result.append((row["one"], row["two"]))
            cursor.close()
            cnx.close()
        return result

