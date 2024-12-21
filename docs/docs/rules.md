# `docs/rules.md`

````markdown
# Reglas de Validación Disponibles

`koma` ofrece una amplia gama de reglas de validación listas para usar. Aquí tienes una lista completa de todas las reglas disponibles y cómo usarlas.
````

## accepted

El campo bajo validación debe ser `yes`, `on`, `1`, o `true`. Esto es útil para validar la aceptación de "Términos de Servicio", por ejemplo.

**Ejemplo:
**

```python
rules = {
    'terms': ['accepted']
}
```

## active_url

El campo bajo validación debe tener un registro A o AAAA válido según la función dns.resolver.query de .

Ejemplo:


```python
rules = {
'website': ['active_url']
}
```

## after:date

El campo bajo validación debe ser un valor posterior a la fecha dada.

Ejemplo:


```python
rules = {
'start_date': ['date'],
'end_date': ['date', 'after:start_date']
}

```

## after_or_equal:date

El campo bajo validación debe ser un valor posterior o igual a la fecha dada.

Ejemplo:

```python
rules = {
'start_date': ['date'],
'end_date': ['date', 'after_or_equal:start_date']
}

```

## alpha

El campo bajo validación debe consistir completamente de caracteres alfabéticos.

Ejemplo:

```python
rules = {
'name': ['alpha']
}

```

## alpha_dash

El campo bajo validación puede tener caracteres alfanuméricos, así como guiones y guiones bajos.

Ejemplo:

```python
rules = {
'username': ['alpha_dash']
}

```

## alpha_num

El campo bajo validación debe consistir completamente de caracteres alfanuméricos.

Ejemplo:

```python
rules = {
'username': ['alpha_num']
}
```
## array

El campo bajo validación debe ser un array de .

Ejemplo:

```python
rules = {
'hobbies': ['array']
}
```
## bail

Detiene la ejecución de las reglas de validación para un atributo después del primer fallo de validación.

Ejemplo:

```python
rules = {
'email': ['bail', 'required', 'email']
}
```
## before:date

El campo bajo validación debe ser un valor anterior a la fecha dada.

Ejemplo:

```python
rules = {
'end_date': ['date'],
'start_date': ['date', 'before:end_date']
}````
## before_or_equal:date

El campo bajo validación debe ser un valor anterior o igual a la fecha dada.

Ejemplo:

```python
rules = {
'end_date': ['date'],
'start_date': ['date', 'before_or_equal:end_date']
}````
## between:min,max

El campo bajo validación debe tener un tamaño entre min y max (inclusive).

Ejemplo:

```python
rules = {
'age': ['between:18,65']
}
```
## boolean

El campo bajo validación debe poder ser interpretado como un valor booleano. Los valores aceptados son true, false, 1, 0, "1", y "0".

Ejemplo:

```python
rules = {
'is_active': ['boolean']
}
```
## confirmed

El campo bajo validación debe tener un campo coincidente de {field}\_confirmation. Por ejemplo, si el campo bajo validación es password, debe haber un campo password_confirmation presente en los datos.

Ejemplo:

```python
rules = {
'password': ['confirmed']
}
```
## date

El campo bajo validación debe ser una fecha válida según la función datetime.strptime de .

Ejemplo:

```python
rules = {
'birth_date': ['date']
}
```
## date_equals:date

El campo bajo validación debe ser igual a la fecha dada.

Ejemplo:

```python
rules = {
'date_of_birth': ['date', 'date_equals:1990-01-01']
}
```
## date_format:format

El campo bajo validación debe coincidir con el formato dado.

Ejemplo:

```python
rules = {
'start_time': ['date_format:H:M']
}
```
## decimal:min,max

El campo bajo validación debe ser numérico y contener la cantidad especificada de decimales.

Ejemplo:

```python
rules = {
'price': ['decimal:2,4']
}
```
## declined

El campo bajo validación debe ser "no", "off", 0, o false.

Ejemplo:

```python
rules = {
'terms_accepted': ['declined']
}
```
## declined_if:otro_campo,valor

El campo bajo validación debe ser "no", "off", 0, o false si el otro campo es igual al valor especificado.

Ejemplo:

```python
rules = {
'terms_accepted': ['declined_if:country,US']
}
```
## different:field

El campo bajo validación debe tener un valor diferente al del campo especificado.

Ejemplo:

```python
rules = {
'email': ['different:old_email']
}
```
## digits:value

El campo bajo validación debe ser numérico y tener una longitud exacta de value.

Ejemplo:

```python
rules = {
'zip_code': ['digits:5']
}
```
## digits_between:min,max

El campo bajo validación debe ser numérico y tener una longitud entre min y max.

Ejemplo:

```python
rules = {
'pin_code': ['digits_between:4,6']
}
```
## dimensions

El campo bajo validación debe ser una imagen que cumpla con las restricciones de dimensiones especificadas.

Ejemplo:

```python
rules = {
'avatar': [('dimensions', {'min_width': 100, 'min_height': 200})]
}
```
## distinct

Al trabajar con arrays, el campo bajo validación no debe tener valores duplicados.

Ejemplo:

```python
rules = {
'categories': ['array', 'distinct']
}
```
## email

El campo bajo validación debe estar formateado como una dirección de correo electrónico.

Ejemplo:

```python
rules = {
'email': ['email']
}
```
## ends_with:value1,value2,...

El campo bajo validación debe terminar con uno de los valores dados.

Ejemplo:

```python
rules = {
'filename': ['ends_with:.txt,.pdf,.doc']
}
```
## exclude

El campo bajo validación será excluido de los datos devueltos por validated() y safe().

Ejemplo:

```python
rules = {
'password': ['exclude']
}
```
## exclude_if:otro_campo,valor

El campo bajo validación será excluido de los datos devueltos por validated() y safe() si otro campo es igual a un valor dado.

Ejemplo:

```python
rules = {
'type': ['exclude_if:mode,test']
}
```
## exclude_unless:otro_campo,valor

El campo bajo validación será excluido de los datos devueltos por validated() y safe() a menos que otro campo sea igual a un valor dado.

Ejemplo:

```python
rules = {
'type': ['exclude_unless:mode,production']
}
```
## exclude_with:otro_campo

El campo bajo validación será excluido de los datos devueltos por validated() y safe() si otro campo está presente.

Ejemplo:

```python
rules = {
'token': ['exclude_with:api_key']
}
```
## exclude_without:otro_campo

El campo bajo validación será excluido de los datos devueltos por validated() y safe() si otro campo no está presente.

Ejemplo:

```python
rules = {
'token': ['exclude_without:api_key']
}
```
## exists:tabla,columna

El campo bajo validación debe existir en la tabla y columna de la base de datos especificada. (Nota: Esta regla requiere configuración de la base de datos).

Ejemplo:

```python
rules = {
'category_id': [('exists', 'categories', 'id')]
}
```
## file

El campo bajo validación debe ser un archivo subido exitosamente.

Ejemplo:

```python
rules = {
'document': ['file']
}
```
## filled

El campo bajo validación no debe estar vacío cuando está presente.

## Ejemplo:

```python
rules = {
'email': ['filled', 'email']
}
```
## gt:field

El campo bajo validación debe ser mayor que el campo dado.

Ejemplo:

```python
rules = {
'start_time': ['date'],
'end_time': ['date', 'gt:start_time']
}````
## gte:field

El campo bajo validación debe ser mayor o igual que el campo dado.

Ejemplo:

```python
rules = {
'start_time': ['date'],
'end_time': ['date', 'gte:start_time']
}````
## hex_color

El campo bajo validación debe ser un color hexadecimal válido.

Ejemplo:

```python
rules = {
'color': ['hex_color']
}
```
## image

El campo bajo validación debe ser una imagen (jpeg, png, bmp, gif, svg, o webp).

Ejemplo:

```python
rules = {
'avatar': ['image']
}
```
in_array:otro_campo.\*
El campo bajo validación debe existir en los valores de otro campo array.

Ejemplo:

```python
rules = {
'item_id': ['in_array:items.*.id']
}
```
integer
El campo bajo validación debe ser un número entero.

Ejemplo:

```python
rules = {
'age': ['integer']
}
```
ip
El campo bajo validación debe ser una dirección IP válida.

Ejemplo:

```python
rules = {
'ip_address': ['ip']
}
```
ipv4
El campo bajo validación debe ser una dirección IPv4 válida.

Ejemplo:

```python
rules = {
'ip_address': ['ipv4']
}
```
ipv6
El campo bajo validación debe ser una dirección IPv6 válida.

Ejemplo:

```python
rules = {
'ip_address': ['ipv6']
}
```
json
El campo bajo validación debe ser una cadena JSON válida.

Ejemplo:

```python
rules = {
'settings': ['json']
}
```
lt:field
El campo bajo validación debe ser menor que el campo dado.

Ejemplo:

```python
rules = {
'end_time': ['date'],
'start_time': ['date', 'lt:end_time']
}````
lte:field
El campo bajo validación debe ser menor o igual que el campo dado.

Ejemplo:

```python
rules = {
'end_time': ['date'],
'start_time': ['date', 'lte:end_time']
}````
mac_address
El campo bajo validación debe ser una dirección MAC válida.

Ejemplo:

```python
rules = {
'mac': ['mac_address']
}
```
max:value
El campo bajo validación no debe ser mayor que value.

Ejemplo:

```python
rules = {
'name': ['max:255']
}
```
max_digits:value
El campo bajo validación no debe tener más de value dígitos.

Ejemplo:

```python
rules = {
'code': ['max_digits:10']
}
```
mimes:foo,bar,...
El archivo bajo validación debe tener un tipo MIME correspondiente a una de las extensiones listadas.

Ejemplo:

```python
rules = {
'photo': ['mimes:jpeg,png,gif']
}
```
mimetypes:text/plain,...
El archivo bajo validación debe coincidir con uno de los tipos MIME dados.

Ejemplo:

```python
rules = {
'document': ['mimetypes:application/pdf,application/msword']
}
```
min:value
El campo bajo validación debe ser al menos value.

Ejemplo:

```python
rules = {
'age': ['min:18']
}
```
min_digits:value
El campo bajo validación debe tener al menos value dígitos.

Ejemplo:

```python
rules = {
'code': ['min_digits:6']
}
```
missing
El campo bajo validación no debe estar presente en los datos de entrada.

Ejemplo:

```python
rules = {
'token': ['missing']
}
```
missing_if:otro_campo,valor
El campo bajo validación no debe estar presente si otro campo es igual a un valor dado.

Ejemplo:

```python
rules = {
'token': ['missing_if:auth_type,none']
}
```
missing_unless:otro_campo,valor
El campo bajo validación no debe estar presente a menos que otro campo sea igual a un valor dado.

Ejemplo:

```python
rules = {
'token': ['missing_unless:auth_type,api']
}
```
missing_with:otro_campo
El campo bajo validación no debe estar presente cuando otro campo especificado está presente.

Ejemplo:

```python
rules = {
'token': ['missing_with:api_key']
}
```
missing_with_all:otro_campo,otro_campo_2,...
El campo bajo validación no debe estar presente cuando todos los otros campos especificados están presentes.

Ejemplo:

```python
rules = {
'token': ['missing_with_all:api_key,secret_key']
}
```
multiple_of:value
El campo bajo validación debe ser un múltiplo de value.

Ejemplo:

```python
rules = {
'quantity': ['multiple_of:5']
}
```
not_in:value1,value2,...
El campo bajo validación no debe estar en la lista de valores dada.

Ejemplo:

```python
rules = {
'category': ['not_in:admin,superuser']
}
```
not_regex:pattern
El campo bajo validación no debe coincidir con el patrón de expresión regular dado.

Ejemplo:

```python
rules = {
'code': ['not_regex:/[a-z]/']
}
```
nullable
El campo bajo validación puede ser nulo.

Ejemplo:

```python
rules = {
'middle_name': ['nullable', 'string']
}
```
numeric
El campo bajo validación debe ser numérico.

Ejemplo:

```python
rules = {
'age': ['numeric']
}
```
password
El campo bajo validación debe ser una contraseña que cumpla ciertos requisitos.

Ejemplo:

```python
rules = {
'password': [('password', {'min_length': 8, 'letters': True, 'mixed_case': True, 'numbers': True, 'symbols': True})]
}
```
present
El campo bajo validación debe estar presente en los datos de entrada, pero puede estar vacío.

Ejemplo:

```python
rules = {
'name': ['present']
}
```
prohibited
El campo bajo validación debe estar vacío o no presente.

Ejemplo:

```python
rules = {
'secret': ['prohibited']
}
```
prohibited_if:otro_campo,valor,...
El campo bajo validación debe estar vacío o no presente si otro campo es igual a un valor dado.

Ejemplo:

```python
rules = {
'access_token': ['prohibited_if:auth_type,none']
}
```
prohibited_unless:otro_campo,valor,...
El campo bajo validación debe estar vacío o no presente a menos que otro campo sea igual a un valor dado.

Ejemplo:

```python
rules = {
'access_token': ['prohibited_unless:auth_type,api']
}
```
prohibits:otro_campo,...
Si el campo bajo validación está presente, todos los campos especificados no deben estar presentes.

Ejemplo:

```python
rules = {
'access_token': ['prohibits:refresh_token,session_id']
}
```
regex:pattern
El campo bajo validación debe coincidir con el patrón de expresión regular dado.

Ejemplo:

```python
rules = {
'code': [('regex', '/^[a-z]+$/i')]
}
```
required
El campo bajo validación debe estar presente en los datos de entrada y no vacío.

Ejemplo:

```python
rules = {
'name': ['required']
}
```
required_array_keys:key1,key2,...
El campo bajo validación debe ser un array y contener las claves especificadas.

Ejemplo:

```python
rules = {
'user': [('required_array_keys', 'name', 'email')]
}
```
required_if:otro_campo,valor,...
El campo bajo validación es obligatorio si otro campo es igual a un valor dado.

Ejemplo:

```python
rules = {
'state': ['required_if:country,US']
}
```
required_if_accepted:otro_campo
El campo bajo validación es obligatorio si otro campo es yes, on, 1, o true.

Ejemplo:

```python
rules = {
'terms_accepted': ['required_if_accepted:privacy_policy']
}
```
required_unless:otro_campo,valor,...
El campo bajo validación es obligatorio a menos que otro campo sea igual a un valor dado.

Ejemplo:

```python
rules = {
'state': ['required_unless:country,CA']
}
```
required_with:otro_campo,...
El campo bajo validación es obligatorio cuando alguno de los otros campos especificados están presentes.

Ejemplo:

```python
rules = {
'city': ['required_with:state,country']
}
```
required_with_all:otro_campo,otro_campo_2,...
El campo bajo validación es obligatorio cuando todos los otros campos especificados están presentes.

Ejemplo:

```python
rules = {
'city': ['required_with_all:state,country']
}
```
required_without:otro_campo,...
El campo bajo validación es obligatorio cuando alguno de los otros campos especificados no están presentes.

Ejemplo:

```python
rules = {
'email': ['required_without:phone']
}
```
required_without_all:otro_campo,otro_campo_2,...
El campo bajo validación es obligatorio cuando ninguno de los otros campos especificados están presentes.

Ejemplo:

```python
rules = {
'email': ['required_without_all:phone,cell']
}
```
same:field
El campo bajo validación y el campo dado deben coincidir.

Ejemplo:

```python
rules = {
'password': ['required', 'same:password_confirmation']
}
```
size:value
El campo bajo validación debe tener un tamaño igual a value.

Ejemplo:

```python
rules = {
'code': ['size:10']
}
```
starts_with:value1,value2,...
El campo bajo validación debe comenzar con uno de los valores dados.

Ejemplo:

```python
rules = {
'name': ['starts_with:Mr.,Ms.,Dr.']
}
```
string
El campo bajo validación debe ser una cadena.

Ejemplo:

```python
rules = {
'name': ['string']
}
```
timezone
El campo bajo validación debe ser una zona horaria válida.

Ejemplo:

```python
rules = {
'timezone': ['timezone']
}
```
unique:tabla,columna,except,idColumn
El campo bajo validación debe ser único en la tabla y columna de la base de datos especificada. (Nota: Esta regla requiere configuración de la base de datos).

Ejemplo:

```python
rules = {
'email': [('unique', 'users', 'email', 'NULL', 'id')]
}
```
url
El campo bajo validación debe ser una URL válida.

Ejemplo:

```python
rules = {
'website': ['url']
}
```
uuid
El campo bajo validación debe ser un UUID válido.

Ejemplo:

```python
rules = {
'id': ['uuid']
}
```