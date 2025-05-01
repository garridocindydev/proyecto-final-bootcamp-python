# Sistema de Incautación Judicial

Sistema web para la gestión de incautaciones judiciales, desarrollado con Flask y MySQL.

## 🚀 Características

- Sistema de autenticación basado en RUT chileno
- Roles de usuario:
  - Administrador
  - Financiera
  - Abogado
  - Incautador
- Panel de administración para gestión de usuarios
- Validación de RUT chileno
- Seguridad con contraseñas hasheadas
- Manejo de sesiones

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

## 📝 Funcionalidades

### Administrador
- Crear nuevos usuarios
- Ver lista de usuarios
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

## 📄 Licencia

Este proyecto está bajo la Licencia [NOMBRE_DE_LA_LICENCIA].
