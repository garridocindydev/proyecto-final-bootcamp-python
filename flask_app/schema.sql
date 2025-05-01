CREATE DATABASE IF NOT EXISTS incautacion_judicial_db;
USE incautacion_judicial_db;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rut VARCHAR(12) UNIQUE NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    rol ENUM('admin', 'financiera', 'abogado', 'incautador') NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Crear el usuario administrador inicial
INSERT INTO usuarios (rut, nombre, email, password, rol)
VALUES (
    '11111111-1',
    'Administrador',
    'admin@sistema.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewFuWQSDUYfGw1Vy', -- Contraseña: admin123
    'admin'
);
