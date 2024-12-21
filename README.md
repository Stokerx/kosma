# Kosma: Biblioteca de Validación en Python

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`kosma` es una biblioteca de validación para Python inspirada en el sistema de validación de Laravel. Proporciona una forma flexible y extensible de validar datos en tus aplicaciones Python, con una amplia gama de reglas de validación listas para usar y la posibilidad de crear tus propias reglas personalizadas.

## Características

-   Amplia variedad de reglas de validación incorporadas.
-   Soporte para reglas de validación personalizadas.
-   Manejo de mensajes de error personalizados.
-   Fácil integración con cualquier proyecto Python.
-   Inspirado en el sistema de validación de Laravel.
-   Compatible con Python 3.12

## Instalación

Para instalar `kosma`, utiliza pip:

```bash
pip install kosma
```

# Uso
Aquí tienes un ejemplo básico de cómo usar kosma:

```python
from kosma import Validator
data = {
    'email': 'test@example.com',
    'name': 'John Doe',
    'age': 25,
    'password': 'Password123',
    'password_confirmation': 'Password123',
    'city': '   ',
    'photo': 'ruta/a/la/foto.jpg',
    'hobbies': ['leer', 'programar', 'viajar'],
    'social_links': {
        'twitter': 'https://twitter.com/johndoe',
        'facebook': 'https://facebook.com/johndoe',
    }
}

rules = {
    'email': ['required', 'email'],
    'name': ['required', 'string', 'max:255'],
    'age': ['required', 'integer', 'min:18'],
    'password': ['required', 'confirmed', ('min', 8), ('regex', r'[A-Z]'), ('regex', r'[0-9]')],
    'city': ['filled'],
    'photo': [('image'), ('dimensions', {'min_width': 100, 'min_height': 200})],
    'hobbies': ['array', ('min', 1)],
    'social_links.twitter': ['url'],
    'social_links.facebook': ['url'],
}

messages = {
    'email.required': 'El campo correo electrónico es obligatorio.',
    'email.email': 'El correo electrónico no es válido.',
    'name.required': 'El campo nombre es obligatorio.',
    'age.min': 'Debes ser mayor de 18 años.',
    'password.regex': 'La contraseña debe contener al menos una letra mayúscula y un número.',
    'password.min': 'La contraseña debe tener al menos 8 caracteres.',
    'photo.image': 'El archivo debe ser una imagen.',
    'photo.dimensions': 'La imagen debe tener al menos 100px de ancho y 200px de alto.',
    'hobbies.array': 'El campo hobbies debe ser un array.',
    'hobbies.min': 'Debes tener al menos un hobby.',
    'social_links.twitter.url': 'El enlace de Twitter no es una URL válida.',
    'social_links.facebook.url': 'El enlace de Facebook no es una URL válida.',
}

validator = Validator(data, rules, messages)

if validator.passes():
    validated_data = validator.validated()
    print("Datos validados:", validated_data)
else:
    errors = validator.errors()
    print("Errores de validación:", errors)
```

# Reglas de Validación Disponibles
kosma proporciona una amplia gama de reglas de validación, que incluyen:

## Reglas de Validación Disponibles

| Regla | Descripción |
|-------|-------------|
| accepted | El campo debe ser yes, on, 1, o true. |
| active_url | El campo debe ser una URL activa. |
| after:date | El campo debe ser una fecha posterior a la fecha dada. |
| after_or_equal:date | El campo debe ser una fecha posterior o igual a la fecha dada. |
| alpha | El campo solo debe contener caracteres alfabéticos. |
| alpha_dash | El campo solo debe contener caracteres alfanuméricos, guiones y guiones bajos. |
| alpha_num | El campo solo debe contener caracteres alfanuméricos. |
| array | El campo debe ser un array. |
| bail | Detiene la ejecución de las reglas de validación para un atributo después del primer fallo. |
| before:date | El campo debe ser una fecha anterior a la fecha dada. |
| before_or_equal:date | El campo debe ser una fecha anterior o igual a la fecha dada. |
| between:min,max | El campo debe tener un tamaño entre min y max. |
| boolean | El campo debe ser booleano (true, false, 1, 0, "1", "0"). |
| confirmed | El campo debe tener un campo coincidente de campo_confirmation. |
| date | El campo debe ser una fecha válida. |
| date_equals:date | El campo debe ser igual a la fecha dada. |
| date_format:format | El campo debe coincidir con el formato de fecha dado. |
| decimal:min,max | El campo debe ser numérico y tener el número especificado de decimales. |
| declined | El campo debe ser no, off, 0, o false. |
| declined_if:otro_campo,valor,... | El campo debe ser no, off, 0, o false si otro campo es igual a un valor dado. |
| different:field | El campo debe tener un valor diferente al del campo especificado. |
| digits:value | El campo debe ser numérico y tener una longitud exacta de value. |
| digits_between:min,max | El campo debe ser numérico y tener una longitud entre min y max. |
| dimensions | El campo debe ser una imagen que cumpla con las restricciones de dimensiones especificadas. |
| distinct | El campo no debe tener valores duplicados cuando se valida un array. |
| email | El campo debe ser una dirección de correo electrónico válida. |
| ends_with:value1,value2,... | El campo debe terminar con uno de los valores dados. |
| exclude | El campo se excluirá del validated_data. |
| exclude_if:otro_campo,valor | El campo se excluirá del validated_data si otro campo es igual a un valor dado. |
| exclude_unless:otro_campo,valor | El campo se excluirá del validated_data a menos que otro campo sea igual a un valor dado. |
| exclude_with:otro_campo | El campo se excluirá del validated_data si otro campo está presente. |
| exclude_without:otro_campo | El campo se excluirá del validated_data si otro campo no está presente. |
| exists:tabla,columna | El campo debe existir en la tabla y columna de la base de datos especificada (requiere configuración). |
| file | El campo debe ser un archivo subido exitosamente. |
| filled | El campo no debe estar vacío cuando está presente. |
| gt:field | El campo debe ser mayor que el campo dado. |
| gte:field | El campo debe ser mayor o igual que el campo dado. |
| hex_color | El campo debe ser un color hexadecimal válido. |
| image | El campo debe ser una imagen (jpeg, png, bmp, gif, svg, o webp). |
| in_array:otro_campo.* | El campo debe existir en otro campo array. |
| integer | El campo debe ser un número entero. |
| ip | El campo debe ser una dirección IP válida. |
| ipv4 | El campo debe ser una dirección IPv4 válida. |
| ipv6 | El campo debe ser una dirección IPv6 válida. |
| json | El campo debe ser una cadena JSON válida. |
| lt:field | El campo debe ser menor que el campo dado. |
| lte:field | El campo debe ser menor o igual que el campo dado. |
| mac_address | El campo debe ser una dirección MAC válida. |
| max:value | El campo no debe ser mayor que value. |
| max_digits:value | El campo no debe tener más de value dígitos. |
| mimes:foo,bar,... | El archivo debe tener una extensión MIME correspondiente a una de las extensiones listadas. |
| mimetypes:text/plain,... | El archivo debe coincidir con uno de los tipos MIME dados. |
| min:value | El campo debe ser al menos value. |
| min_digits:value | El campo debe tener al menos value dígitos. |
| missing | El campo no debe estar presente en los datos de entrada. |
| missing_if:otro_campo,valor,... | El campo no debe estar presente si otro campo es igual a un valor dado. |
| missing_unless:otro_campo,valor | El campo no debe estar presente a menos que otro campo sea igual a un valor dado. |
| missing_with:otro_campo,... | El campo no debe estar presente cuando alguno de los otros campos especificados están presentes. |
| missing_with_all:otro_campo,... | El campo no debe estar presente cuando todos los otros campos especificados están presentes. |
| multiple_of:value | El campo debe ser un múltiplo de value. |
| not_in:value1,value2,... | El campo no debe estar en la lista de valores dada. |
| not_regex:pattern | El campo no debe coincidir con el patrón de expresión regular dado. |
| nullable | El campo puede ser nulo. |
| numeric | El campo debe ser numérico. |
| password | El campo debe cumplir con los requisitos de contraseña. |
| present | El campo debe estar presente en los datos de entrada, pero puede estar vacío. |
| prohibited | El campo no debe estar presente o estar vacío. |
| prohibited_if:otro_campo,valor,... | El campo no debe estar presente o estar vacío si otro campo es igual a un valor dado. |
| prohibited_unless:otro_campo,valor,... | El campo no debe estar presente o estar vacío a menos que otro campo sea igual a un valor dado. |
| prohibits:otro_campo,... | El campo no debe estar presente si alguno de los otros campos especificados está presente. |
| regex:pattern | El campo debe coincidir con el patrón de expresión regular dado. |
| required | El campo es obligatorio. |
| required_array_keys:foo,bar,... | El campo debe ser una matriz y contener las claves especificadas. |
| required_if:otro_campo,valor,... | El campo es obligatorio si otro campo es igual a un valor dado. |
| required_if_accepted:otro_campo | El campo es obligatorio si otro campo es aceptado. |
| required_unless:otro_campo,valor,... | El campo es obligatorio a menos que otro campo sea igual a un valor dado. |
| required_with:otro_campo,... | El campo es obligatorio cuando alguno de los otros campos especificados están presentes. |
| required_with_all:otro_campo,... | El campo es obligatorio cuando todos los otros campos especificados están presentes. |
| required_without:otro_campo,... | El campo es obligatorio cuando alguno de los otros campos especificados no están presentes. |
| required_without_all:otro_campo,... | El campo es obligatorio cuando ninguno de los otros campos especificados están presentes. |
| same:field | El campo y el campo dado deben coincidir. |
| size:value | El campo debe tener un tamaño igual a value. |
| starts_with:value1,value2,... | El campo debe comenzar con uno de los valores dados. |
| string | El campo debe ser una cadena. |
| timezone | El campo debe ser una zona horaria válida. |
| unique:tabla,columna,except,idColumn | El campo debe ser único en la tabla y columna de la base de datos especificada (requiere configuración). |
| uploaded_file:min,max,ext1,ext2,... | El campo debe ser un archivo subido exitosamente con las restricciones dadas. |
| url | El campo debe ser una URL válida. |
| uuid | El campo debe ser un UUID válido. |

## Contribuciones

Las contribuciones son bienvenidas. Por favor, envía un Pull Request o crea un Issue para discutir los cambios propuestos.

Licencia
kosma está liberado bajo la Licencia MIT.

Este README proporciona una descripción general de la biblioteca `kosma`, cómo instalarla, un ejemplo de uso y una lista de todas las reglas de validación disponibles. También incluye secciones sobre contribuciones y la licencia del proyecto. Puedes personalizarlo aún más con información adicional, como la documentación detallada de cada regla, ejemplos de uso avanzados, y cualquier otra información que consideres relevante para los usuarios de tu biblioteca.
