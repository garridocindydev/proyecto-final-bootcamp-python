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

-- Mensaje de confirmación
SELECT 'Migración completada exitosamente.' as mensaje;
