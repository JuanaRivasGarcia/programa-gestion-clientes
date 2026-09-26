# Programa de gestión de clientes

## Descripción

Aplicación de terminal diseñada para gestionar clientes en una consulta sanitaria (fisioterapia, osteopatía, quiromasaje, reeducación corporal...). Agrega datos personales, dolencias, citas y observaciones.

## Funcionalidades

- Crear y cargar clientes
- Registar dolencias con seguimiento de estado (Activa/Resuelta)
- Añadir citas y observaciones

## Requisitos

- Python 3.x
- No tiene dependencias externas, solo librerías estándar.

## Uso

```bash
python menu_interactivo.py
```

## Estructura del proyecto

- `modelos.py` - Clases del dominio(Cita, Dolencia, Cliente)
- `repositorio.py` - Persistencia en JSON
- `menu_interactivo.py` - Interfaz del menú

## Decisiones de diseño

- **Separación de responsabilidades**: El proyecto está dividido en tres capas individuales - el modelo(`modelo.py`), la persistencia(`repositorio.py`) y la interfaz(`menu_interactivo.py`) - siguiendo el Principio de Responsabilidad Única de SOLID.

- **Composición**: Un cliente tiene dolencias y citas, cada dolencia tiene sus propias observaciones. Favorece la composición frente a la herencia.

- **Patrón repositorio**: Toda la persistencia está aislada en la clase 'RepositorioClientes', permitiendo cambiar el sistema de almacenamiento(por ejemplo, de JSON a SQLite) sin tocar el modelo ni la interfaz.

- **Validación en el modelo**: Las fechas se validan en las propias clases(mediante 'property' y setters), no en la interfaz, de modo que un objeto no puede existir en un estado inválido.

## Futuras mejoras

- Migración de la persistencia de JSON a una base de datos(SQLite).
- Validaciones adicionales(fechas no futuras, campos obligatorios).
- Interfaz gráfica o web.
