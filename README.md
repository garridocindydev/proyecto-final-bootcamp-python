# Sistema de Incautación Judicial 🚗

Sistema web integral para la gestión de incautaciones judiciales, desarrollado con Flask y MySQL. Permite la coordinación entre estudios jurídicos, abogados, e incautadores para la gestión eficiente de juicios e incautaciones de vehículos.

## 🚀 Características Principales

### Sistema Multi-Rol
- **Administrador**: Gestión completa del sistema y usuarios
- **Financiera**: Registro y seguimiento de juicios
- **Super Abogado**: Supervisión de casos y asignación de abogados
- **Abogado**: Gestión de casos y asignación de incautadores
- **Incautador**: Ejecución y registro de incautaciones

### Gestión de Juicios
- Registro detallado de juicios con información del tribunal
- Asignación de juicios a estudios jurídicos
- Seguimiento del estado de cada juicio
- Sistema de comentarios y observaciones

### Incautaciones
- Asignación de incautadores a juicios específicos
- Registro de patentes y detalles de vehículos
- Sistema de estados (Pendiente, En_Proceso, Ejecutado, Fallido)
- Comentarios y reportes de progreso

### Seguridad y Validación
- Autenticación basada en RUT chileno
- Contraseñas hasheadas con bcrypt
- Protección de rutas por rol
- Validación de datos en tiempo real

## 📋 Requisitos Previos

- Python 3.x
- MySQL
- pip (gestor de paquetes de Python)

## 🔧 Instalación

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
```

2. Crear un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar la base de datos:
- Crear una base de datos MySQL
- Ejecutar el script `flask_app/schema.sql`
- Configurar las credenciales en `flask_app/config/mysqlconnection.py`

5. Iniciar el servidor:
```bash
python server.py
```

## 🔐 Credenciales por Defecto

- **Administrador**
  - RUT: 11111111-1
  - Email: admin@sistema.com
  - Contraseña: admin123

## 🏗️ Estructura del Proyecto

```
proyecto-final-bootcamp-python/
├── flask_app/
│   ├── config/
│   │   ├── __init__.py
│   │   └── mysqlconnection.py
│   ├── controllers/
│   │   └── usuarios.py
│   ├── models/
│   │   └── usuario.py
│   ├── templates/
│   │   ├── admin/
│   │   │   ├── nuevo_usuario.html
│   │   │   └── usuarios.html
│   │   └── login.html
│   └── __init__.py
├── requirements.txt
└── server.py
```

## 🔒 Seguridad

- Contraseñas hasheadas con bcrypt
- Validación de RUT chileno
- Protección de rutas administrativas
- Manejo seguro de sesiones
- Prevención de inyección SQL

## 🛠️ Tecnologías Utilizadas

- **Backend**: Flask (Python)
- **Base de Datos**: MySQL
- **Seguridad**: Flask-Bcrypt
- **Frontend**: Bootstrap
- **Plantillas**: Jinja2

## 📝 Funcionalidades Detalladas por Rol

### Administrador 👨‍💼
- **Gestión de Usuarios**
  - Crear, editar y eliminar usuarios
  - Asignar roles y estudios jurídicos
  - Ver historial de actividades
- **Gestión de Estudios**
  - Crear y administrar estudios jurídicos
  - Asignar abogados a estudios

### Financiera 💰
- **Gestión de Juicios**
  - Registrar nuevos juicios
  - Asignar juicios a estudios
  - Actualizar información de pagos
  - Ver estadísticas y reportes

### Super Abogado ⚖️
- **Supervisión de Casos**
  - Ver todos los juicios del estudio
  - Asignar casos a abogados
  - Monitorear progreso de incautaciones
  - Ver comentarios y actualizaciones

### Abogado 👨‍⚖️
- **Gestión de Casos**
  - Ver juicios asignados
  - Asignar incautadores
  - Monitorear estado de incautaciones
  - Ver comentarios de incautadores

### Incautador 🚙
- **Gestión de Incautaciones**
  - Ver asignaciones pendientes
  - Actualizar estado de incautaciones
  - Agregar comentarios y observaciones
  - Registrar éxitos o problemas

## 💾 Operaciones CRUD

### Usuarios
```python
# Create: Crear nuevo usuario
POST /admin/usuarios/nuevo

# Read: Ver usuarios
GET /admin/usuarios

# Update: Actualizar usuario
POST /admin/usuarios/<id>/editar

# Delete: Eliminar usuario
POST /admin/usuarios/<id>/eliminar
```

### Juicios
```python
# Create: Registrar juicio
POST /financiera/juicios/nuevo

# Read: Ver juicios
GET /financiera/juicios

# Update: Actualizar juicio
POST /financiera/juicios/<id>/editar

# Delete: Eliminar juicio
POST /financiera/juicios/<id>/eliminar
```

### Asignaciones
```python
# Create: Asignar incautador
POST /abogado/juicios/<id>/asignar_incautador

# Read: Ver asignaciones
GET /incautador/asignaciones

# Update: Actualizar estado
POST /incautador/asignacion/<id>/estado

# Delete: Cancelar asignación
POST /abogado/asignaciones/<id>/cancelar
```

### Comentarios
```python
# Create: Agregar comentario
POST /incautador/asignacion/<id>/comentario

# Read: Ver comentarios
GET /abogado/comentarios

# Update: Editar comentario
POST /incautador/comentario/<id>/editar

# Delete: Eliminar comentario
POST /incautador/comentario/<id>/eliminar
```
- Eliminar usuarios
- Gestionar roles

### Usuarios
- Inicio de sesión con RUT
- Acceso a funcionalidades según rol
- Cierre de sesión seguro

## 🔄 Estado del Proyecto

En desarrollo activo. Próximas características:
- [ ] Gestión de incautaciones
- [ ] Reportes y estadísticas
- [ ] Panel de control por rol
- [ ] Sistema de notificaciones

## 👥 Contribuir

Si deseas contribuir al proyecto:
1. Haz un Fork
2. Crea una rama para tu característica
3. Haz commit de tus cambios
4. Haz push a la rama
5. Abre un Pull Request

## 📈 Flujo del Sistema

1. **Registro de Juicio**
   - Financiera registra nuevo juicio
   - Asigna a estudio jurídico

2. **Asignación de Abogado**
   - Super Abogado revisa juicio
   - Asigna a abogado del estudio

3. **Asignación de Incautador**
   - Abogado revisa caso
   - Selecciona y asigna incautador

4. **Proceso de Incautación**
   - Incautador recibe asignación
   - Actualiza estado y agrega comentarios
   - Marca como ejecutado o fallido

5. **Seguimiento**
   - Abogado monitorea progreso
   - Super Abogado supervisa casos
   - Financiera actualiza registros

## 📊 Estadísticas y Reportes

- Dashboard personalizado por rol
- Estadísticas de éxito/fallo
- Tiempos promedio de ejecución
- Reportes por estudio jurídico

## 🔑 Seguridad

### Autenticación
- Validación de RUT chileno
- Contraseñas hasheadas con bcrypt
- Tokens de sesión seguros

### Autorización
- Control de acceso basado en roles
- Protección de rutas sensibles
- Validación de permisos por acción

### Protección de Datos
- Prevención de inyección SQL
- Sanitización de entradas
- Logs de actividad

## 💻 Instalación Detallada

### Requisitos del Sistema
- Python 3.8+
- MySQL 5.7+
- pip y virtualenv

### Configuración de la Base de Datos
1. Crear base de datos:
```sql
CREATE DATABASE incautaciones_judiciales_db;
```

2. Configurar variables de entorno:
```bash
export DB_HOST=localhost
export DB_USER=tu_usuario
export DB_PASS=tu_contraseña
export DB_NAME=incautaciones_judiciales_db
```

### Instalación de Dependencias
```bash
pip install -r requirements.txt
```

## 📄 Documentación API

Consulta la [documentación completa de la API](docs/api.md) para más detalles sobre los endpoints y su uso.

## 👨‍💻 Contribución

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 💬 Soporte

Para dudas o sugerencias:
- Crear un issue en GitHub
- Enviar un correo a soporte@incautaciones.com

## 🔑 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.
