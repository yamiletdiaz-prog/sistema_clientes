# Sistema de Control de Clientes

Aplicación de escritorio desarrollada en Python que permite gestionar clientes mediante una interfaz gráfica (tkinter). Implementa los principios de Programación Orientada a Objetos: encapsulamiento, herencia, polimorfismo y manejo de excepciones.

---

## Estructura del Proyecto

```
sistema_control_clientes/
├── cliente.py           # Clase base Cliente (encapsulamiento, getters/setters, __str__)
├── tipos_clientes.py    # Subclases: ClienteRegular, ClientePremium, ClienteCorporativo
├── gestor_clientes.py   # Lógica CRUD, excepciones personalizadas, persistencia JSON/CSV
├── interfaz.py          # Interfaz gráfica con tkinter
├── main.py              # Punto de entrada (ejecuta tests + abre la GUI)
├── test_gic.py          # 14 pruebas unitarias (unittest)
└── README.md
```

---

## Requisitos

- Python 3.x
- tkinter (incluido en la instalación estándar de Python en Windows)

---

## Ejecución

```bash
python main.py
```

Esto ejecuta las pruebas unitarias y luego abre la interfaz gráfica.

Para ejecutar solo las pruebas:

```bash
python -m unittest test_sistema -v
```

---

## Conceptos de POO Aplicados

### Encapsulamiento

La clase `Cliente` en `cliente.py` utiliza atributos privados (`self.__id`, `self.__nombre`, etc.) accesibles únicamente a través de getters y setters, protegiendo el estado interno del objeto.

```python
class Cliente:
    def __init__(self, id, nombre, email, telefono, direccion):
        self.__id = id
        self.__nombre = nombre
        # ...

    def get_id(self): return self.__id
    def set_nombre(self, nombre): self.__nombre = nombre
```

### Herencia

Las clases `ClienteRegular`, `ClientePremium` y `ClienteCorporativo` en `tipos_clientes.py` heredan de `Cliente`, reutilizando sus atributos y métodos base.

```python
class ClienteRegular(Cliente):
    def __init__(self, id, nombre, email, telefono, direccion, puntos=0):
        super().__init__(id, nombre, email, telefono, direccion)
        self.__puntos = puntos
```

### Polimorfismo

Cada subclase sobreescribe los métodos `calcular_descuento()` y `get_tipo()` con comportamiento propio:

| Clase | `calcular_descuento()` | `get_tipo()` |
|---|---|---|
| `ClienteRegular` | `puntos * 0.01` | `"Regular"` |
| `ClientePremium` | `20.0` | `"Premium"` |
| `ClienteCorporativo` | `30.0` | `"Corporativo"` |

### Método Especial `__str__`

Definido en la clase base `Cliente`, permite representar un objeto como cadena de texto:

```python
def __str__(self):
    return f"{self.__id} - {self.__nombre} ({self.get_tipo()})"
```

---

## Manejo de Errores y Excepciones

Se definieron tres excepciones personalizadas en `gestor_clientes.py`:

- **`ClienteDuplicadoError`**: se lanza al intentar agregar un cliente con un ID ya existente.
- **`ClienteNoEncontradoError`**: se lanza al buscar, eliminar o actualizar un cliente con un ID inexistente.
- **`PersistenciaError`**: se lanza ante errores al guardar/cargar archivos JSON o exportar CSV.

La interfaz gráfica (`interfaz.py`) también valida los datos ingresados por el usuario: campos obligatorios (ID, nombre) y tipo de dato correcto (ID numérico).

---

## Persistencia de Datos

La información se almacena en archivos locales (sin base de datos):

- **Guardar/Cargar JSON**: serializa y deserializa la lista de clientes en formato JSON.
- **Exportar CSV**: genera un archivo CSV con los datos de todos los clientes.

---

## Pruebas Unitarias

El archivo `test_gic.py` contiene 14 pruebas que verifican:

- Agregar clientes y detección de duplicados
- Buscar clientes existentes e inexistentes
- Eliminar clientes
- Actualizar datos
- Cálculo de descuentos por tipo (polimorfismo)
- Guardar y cargar datos en JSON
- Exportar datos a CSV
- Manejo correcto de errores y excepciones

---

## Interfaz Gráfica

La GUI desarrollada con tkinter permite:

- **Agregar** clientes (Regular, Premium, Corporativo)
- **Buscar** clientes por ID
- **Actualizar** datos de un cliente
- **Eliminar** clientes
- **Visualizar** todos los clientes en una tabla
- **Guardar/Cargar** datos en formato JSON
- **Exportar** datos a CSV
