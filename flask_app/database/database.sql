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
    abogado_id INT,
    cuantia DECIMAL(10,2) NOT NULL,
    estado ENUM('Pendiente', 'Asignado', 'Terminado') DEFAULT 'Pendiente',
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
    -- Aseguramos que los abogados y super_abogados tengan estudio asignado
    CONSTRAINT chk_abogado_estudio CHECK (
        (rol NOT IN ('abogado', 'super_abogado')) OR 
        ((rol IN ('abogado', 'super_abogado')) AND estudio_id IS NOT NULL)
    )
);

