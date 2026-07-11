-- 1
SELECT e.nombre, e.apellido, d.nombre AS departamento
FROM empleados e
JOIN departamentos d ON e.id_departamento = d.id;

-- 2
INSERT INTO departamentos (nombre) VALUES ('Legales');

SELECT d.nombre AS departamento, e.nombre AS empleado
FROM departamentos d
LEFT JOIN empleados e ON e.id_departamento = d.id;

-- 3
SELECT d.nombre
FROM departamentos d
LEFT JOIN empleados e ON e.id_departamento = d.id
WHERE e.id IS NULL;

-- 4
SELECT d.nombre, COUNT(e.id) AS cantidad_empleados
FROM departamentos d
LEFT JOIN empleados e ON e.id_departamento = d.id
GROUP BY d.nombre;

-- 5
SELECT e.nombre, e.apellido, d.nombre AS departamento
FROM empleados e
JOIN departamentos d ON e.id_departamento = d.id
ORDER BY e.salario DESC
LIMIT 1;