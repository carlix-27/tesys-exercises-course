SELECT * FROM empleados
WHERE salario > (SELECT AVG(salario) FROM empleados);

-- 2 (subconsulta correlacionada)
SELECT e.nombre, e.salario, e.id_departamento
FROM empleados e
WHERE e.salario > (
    SELECT AVG(e2.salario)
    FROM empleados e2
    WHERE e2.id_departamento = e.id_departamento
);

-- 3
SELECT d.nombre
FROM departamentos d
JOIN empleados e ON e.id_departamento = d.id
GROUP BY d.nombre
ORDER BY AVG(e.salario) DESC
LIMIT 1;

-- 4
SELECT d.nombre
FROM departamentos d
WHERE NOT EXISTS (
    SELECT 1 FROM empleados e WHERE e.id_departamento = d.id
);