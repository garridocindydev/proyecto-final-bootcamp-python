-- Migración para agregar el rol super_abogado
-- Primero hacemos un backup de la tabla usuarios
CREATE TABLE usuarios_backup AS SELECT * FROM usuarios;

-- Eliminamos el CONSTRAINT y la columna rol actual
ALTER TABLE usuarios 
DROP CONSTRAINT chk_abogado_estudio,
MODIFY COLUMN rol ENUM('admin', 'financiera', 'super_abogado', 'abogado', 'incautador') NOT NULL;

-- Agregamos el nuevo CONSTRAINT
ALTER TABLE usuarios
ADD CONSTRAINT chk_abogado_estudio CHECK (
    (rol NOT IN ('abogado', 'super_abogado')) OR 
    ((rol IN ('abogado', 'super_abogado')) AND estudio_id IS NOT NULL)
);

-- Script para revertir los cambios en caso de error
/*
-- Eliminamos la tabla usuarios
DROP TABLE IF EXISTS usuarios;

-- Restauramos la tabla desde el backup
CREATE TABLE usuarios AS SELECT * FROM usuarios_backup;

-- Restauramos los índices y constraints
ALTER TABLE usuarios
ADD PRIMARY KEY (id),
ADD UNIQUE (rut),
ADD UNIQUE (email),
ADD FOREIGN KEY (estudio_id) REFERENCES estudios(id),
MODIFY COLUMN id INT AUTO_INCREMENT,
MODIFY COLUMN rol ENUM('admin', 'financiera', 'abogado', 'incautador') NOT NULL,
ADD CONSTRAINT chk_abogado_estudio CHECK (rol != 'abogado' OR (rol = 'abogado' AND estudio_id IS NOT NULL));

-- Eliminamos la tabla de backup
DROP TABLE usuarios_backup;
*/
