-- 1
WITH promedios AS (
    SELECT id_departamento, AVG(salario) AS promedio
    FROM empleados
    GROUP BY id_departamento
)
SELECT d.nombre, p.promedio
FROM promedios p
JOIN departamentos d ON d.id = p.id_departamento
WHERE p.promedio > 600000;

-- 2
SELECT nombre, apellido, id_departamento, salario,
       RANK() OVER (PARTITION BY id_departamento ORDER BY salario DESC) AS ranking
FROM empleados;

-- 3
SELECT nombre, apellido, fecha_ingreso, salario,
       salario - LAG(salario) OVER (ORDER BY fecha_ingreso) AS diferencia
FROM empleados;