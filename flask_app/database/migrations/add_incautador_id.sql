-- Agregar columna incautador_id
ALTER TABLE juicios
ADD COLUMN IF NOT EXISTS incautador_id INT,
ADD CONSTRAINT fk_juicios_incautador
FOREIGN KEY (incautador_id) REFERENCES usuarios(id);
