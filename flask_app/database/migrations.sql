USE incautaciones_judiciales_db;

-- Agregar la columna estudio_id a la tabla usuarios
ALTER TABLE usuarios
ADD COLUMN estudio_id INT,
ADD FOREIGN KEY (estudio_id) REFERENCES estudios(id);

-- Agregar la restricción CHECK para asegurar que solo los abogados tengan estudio asignado
-- Primero aseguramos que no haya datos que violen la restricción
UPDATE usuarios 
SET estudio_id = NULL 
WHERE rol != 'abogado';

-- Luego agregamos la restricción
ALTER TABLE usuarios
ADD CONSTRAINT chk_abogado_estudio 
CHECK (rol != 'abogado' OR (rol = 'abogado' AND estudio_id IS NOT NULL));

-- Agregar columnas de abogado e incautador a la tabla juicios
ALTER TABLE juicios
ADD COLUMN abogado_id INT,
ADD COLUMN incautador_id INT,
ADD FOREIGN KEY (abogado_id) REFERENCES usuarios(id),
ADD FOREIGN KEY (incautador_id) REFERENCES usuarios(id);

-- Crear tabla de mensajes
CREATE TABLE mensajes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    contenido TEXT NOT NULL,
    juicio_id INT NOT NULL,
    emisor_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (juicio_id) REFERENCES juicios(id),
    FOREIGN KEY (emisor_id) REFERENCES usuarios(id)
);

-- Mensaje de confirmación
SELECT 'Migración completada exitosamente.' as mensaje;
