from . import Rule
# Nota: Esta regla es compleja y normalmente se integra con una base de datos.
# Aquí se presenta una versión simplificada para fines ilustrativos.

class Unique(Rule):
    def __init__(self, table, column, ignore=None, id_column='id'):
        self.table = table
        self.column = column
        self.ignore = ignore
        self.id_column = id_column

    def passes(self, attribute, value, parameters, validator):
        # Aquí iría la lógica para conectar con la base de datos y verificar la unicidad
        # Este es solo un placeholder, necesitarías una implementación real con una base de datos
        print(f"Verificando unicidad de {value} en la columna {self.column} de la tabla {self.table}, ignorando ID {self.ignore} en columna {self.id_column}")
        return True  # Retorna True por defecto para propósitos de demostración

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} has already been taken."