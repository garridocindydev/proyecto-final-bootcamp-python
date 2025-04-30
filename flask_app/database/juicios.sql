CREATE TABLE juicios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_pagare VARCHAR(255) NOT NULL,
    rol VARCHAR(255) NOT NULL,
    tribunal VARCHAR(255) NOT NULL,
    estudio INT,
    cuantia DECIMAL(10,2) NOT NULL,
    estado ENUM('Pendiente', 'Asignado', 'Terminado') DEFAULT 'Pendiente',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (estudio) REFERENCES estudios(id)
);
