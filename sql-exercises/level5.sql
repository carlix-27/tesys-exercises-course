-- 1
INSERT INTO empleados (nombre, apellido, salario, id_departamento, fecha_ingreso)
VALUES ('Rocío', 'Vega', 620000, 4, '2024-05-01');

-- 2
UPDATE empleados
SET salario = salario * 1.1
WHERE id_departamento = 1;

-- 3
DELETE FROM empleados WHERE id_departamento IS NULL;

-- 4
ALTER TABLE empleados ADD COLUMN email VARCHAR(100);

-- 5
ALTER TABLE empleados RENAME COLUMN apellido TO apellido_paterno;
