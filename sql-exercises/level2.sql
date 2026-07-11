-- 1
SELECT COUNT(*) FROM empleados;

-- 2
SELECT AVG(salario) FROM empleados;

-- 3
SELECT MAX(salario), MIN(salario) FROM empleados;

-- 4
SELECT id_departamento, COUNT(*) FROM empleados GROUP BY id_departamento;

-- 5
SELECT id_departamento, AVG(salario) FROM empleados GROUP BY id_departamento;

-- 6
SELECT id_departamento, AVG(salario) AS promedio
FROM empleados
GROUP BY id_departamento
HAVING AVG(salario) > 650000;

-- 7
SELECT EXTRACT(YEAR FROM fecha_ingreso) AS year, COUNT(*)
FROM empleados
GROUP BY year
ORDER BY year;