from . import Rule
# Nota: Esta regla es compleja y normalmente se integra con una base de datos.
# Aquí se presenta una versión simplificada para fines ilustrativos.

class Exists(Rule):
    def __init__(self, table, column):
        self.table = table
        self.column = column

    def passes(self, attribute, value, parameters, validator):
        # Aquí iría la lógica para conectar con la base de datos y verificar la existencia
        # Este es solo un placeholder, necesitarías una implementación real con una base de datos
        print(f"Verificando si {value} existe en la columna {self.column} de la tabla {self.table}")
        return True  # Retorna True por defecto para propósitos de demostración

    def message(self, attribute, value, parameters, validator):
        return f"The selected {attribute} is invalid."