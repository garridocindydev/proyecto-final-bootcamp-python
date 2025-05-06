-- Crear y usar la base de datos
CREATE DATABASE IF NOT EXISTS incautaciones_judiciales_db;
USE incautaciones_judiciales_db;

-- Tabla de estudios jurídicos
CREATE TABLE IF NOT EXISTS estudios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla de juicios
CREATE TABLE IF NOT EXISTS juicios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_pagare VARCHAR(255) NOT NULL,
    rol VARCHAR(255) NOT NULL,
    tribunal VARCHAR(255) NOT NULL,
    estudio INT,
    patente_vehiculo VARCHAR(10) NOT NULL,
    abogado_id INT,
    estado ENUM('Pendiente', 'Asignado', 'Ejecutado', 'Fallido') DEFAULT 'Pendiente',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (estudio) REFERENCES estudios(id),
    FOREIGN KEY (abogado_id) REFERENCES usuarios(id)
);

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rut VARCHAR(12) UNIQUE NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    rol ENUM('admin', 'financiera', 'super_abogado', 'abogado', 'incautador') NOT NULL,
    estudio_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (estudio_id) REFERENCES estudios(id),
    CONSTRAINT chk_abogado_estudio CHECK (rol != 'abogado' OR (rol = 'abogado' AND estudio_id IS NOT NULL))
);

-- Tabla de asignaciones de juicios a incautadores
CREATE TABLE IF NOT EXISTS asignaciones_juicios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    juicio_id INT NOT NULL,
    abogado_id INT NOT NULL,
    incautador_id INT NOT NULL,
    fecha_asignacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_ejecucion DATETIME,
    estado ENUM('Pendiente', 'En_Proceso', 'Ejecutado', 'Fallido') DEFAULT 'Pendiente',
    observaciones TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (juicio_id) REFERENCES juicios(id),
    FOREIGN KEY (abogado_id) REFERENCES usuarios(id),
    FOREIGN KEY (incautador_id) REFERENCES usuarios(id)
);

-- Tabla de comentarios de incautadores
CREATE TABLE IF NOT EXISTS comentarios_incautador (
    id INT AUTO_INCREMENT PRIMARY KEY,
    asignacion_id INT NOT NULL,
    incautador_id INT NOT NULL,
    comentario TEXT NOT NULL,
    tipo_comentario ENUM('Avance', 'Problema', 'Éxito', 'Otro') NOT NULL,
    fecha_comentario DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (asignacion_id) REFERENCES asignaciones_juicios(id),
    FOREIGN KEY (incautador_id) REFERENCES usuarios(id)
);

-- Insertar datos de prueba

-- Crear el usuario administrador inicial
INSERT INTO usuarios (rut, nombre, email, password, rol)
VALUES (
    'admin',
    'Administrador',
    'admin@sistema.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewFuWQSDUYfGw1Vy', -- Contraseña: admin123
    'admin'
);

-- Insertar un estudio jurídico de prueba
INSERT INTO estudios (nombre) VALUES ('Estudio Jurídico ABC');

-- Insertar usuarios de prueba
INSERT INTO usuarios (rut, nombre, email, password, rol, estudio_id) VALUES
('12345678-9', 'Juan Abogado', 'abogado@test.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewFuWQSDUYfGw1Vy', 'abogado', 1),
('98765432-1', 'Pedro Incautador', 'incautador@test.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewFuWQSDUYfGw1Vy', 'incautador', NULL);

-- Insertar juicios de prueba
INSERT INTO juicios (id_pagare, rol, tribunal, estudio, patente_vehiculo, marca_vehiculo, modelo_vehiculo) VALUES
('PAG001', 'C-1234-2023', '1° Juzgado Civil', 1, 'ABCD12', 'Toyota', 'Corolla'),
('PAG002', 'C-5678-2023', '2° Juzgado Civil', 1, 'WXYZ98', 'Nissan', 'Versa'),
('PAG003', 'C-9012-2023', '3° Juzgado Civil', 1, 'EFGH34', 'Hyundai', 'Accent');

-- Insertar asignaciones de prueba
INSERT INTO asignaciones_juicios (juicio_id, abogado_id, incautador_id, estado) VALUES
(1, 2, 3, 'Pendiente'),
(2, 2, 3, 'En_Proceso'),
(3, 2, 3, 'Pendiente');

-- Insertar algunos comentarios de prueba
INSERT INTO comentarios_incautador (asignacion_id, incautador_id, comentario, tipo_comentario) VALUES
(1, 3, 'Iniciando búsqueda del vehículo', 'Avance'),
(2, 3, 'Vehículo localizado en estacionamiento', 'Éxito'),
(2, 3, 'Esperando grúa para el retiro', 'Avance');
    -- Aseguramos que los abogados y super_abogados tengan estudio asignado
    CONSTRAINT chk_abogado_estudio CHECK (
        (rol NOT IN ('abogado', 'super_abogado')) OR 
        ((rol IN ('abogado', 'super_abogado')) AND estudio_id IS NOT NULL)
    )
);

