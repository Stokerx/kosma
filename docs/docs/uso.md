
### `docs/uso.md`

```markdown
# Uso Básico

`py-validator` está diseñado para ser fácil de usar y flexible. Aquí te mostramos cómo puedes empezar a usarlo en tus proyectos.

## Importando el Validador

Primero, importa la clase `Kosma` en tu script de Python:

```python
from kosma import Validator
```

## Creando una Instancia del Validador
Para usar el validador, primero necesitas crear una instancia de la clase Validator, pasando los datos a validar, las reglas de validación y opcionalmente, mensajes de error personalizados:

```python
data = {
    'email': 'test@example.com',
    'name': 'John Doe',
    'age': 25
}

rules = {
    'email': ['required', 'email'],
    'name': ['required', 'string', 'max:255'],
    'age': ['required', 'integer', 'min:18']
}

messages = {
    'email.required': 'El campo correo electrónico es obligatorio.',
    'email.email': 'El correo electrónico no es válido.',
    'name.required': 'El campo nombre es obligatorio.',
    'age.min': 'Debes ser mayor de 18 años.'
}

validator = Validator(data, rules, messages)
```

## Ejecutando la Validación
Puedes verificar si los datos pasan las reglas de validación usando el método passes():

```python
if validator.passes():
    print("Los datos son válidos.")
else:
    errors = validator.errors()
    print("Errores de validación:", errors)
```

## O si prefieres una excepción en caso de fallo:

```python
try:
    validator.validate()
    print("Los datos son válidos.")
except ValidationException as e:
    print("Errores de validación:", e.errors)
```

## Accediendo a los Datos Validados
Si la validación es exitosa, puedes acceder a los datos validados usando el método validated():
```python
validated_data = validator.validated()
print("Datos validados:", validated_data)
```

## Reglas de Validación Personalizadas
Puedes extender kosma con tus propias reglas de validación. Consulta la sección Personalización para más detalles.

### Ejemplo Completo
Aquí tienes un ejemplo completo de cómo usar kosma:

```python
from kosma import Validator
from kosma.exceptions import ValidationException

data = {
    'email': 'test@example.com',
    'name': 'John Doe',
    'age': 25
}

rules = {
    'email': ['required', 'email'],
    'name': ['required', 'string', 'max:255'],
    'age': ['required', 'integer', 'min:18']
}

validator = Validator(data, rules)

try:
    validated_data = validator.validate()
    print("Datos validados:", validated_data)
except ValidationException as e:
    print("Errores de validación:", e.errors)
```