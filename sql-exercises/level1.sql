SELECT * FROM empleados;

SELECT nombre, apellido FROM empleados;

SELECT * FROM empleados WHERE salario > 650000;

SELECT * FROM empleados WHERE id_departamento = 1;

SELECT * FROM empleados ORDER BY salario DESC;

SELECT * FROM empleados ORDER BY salario DESC LIMIT 3;

SELECT * FROM empleados WHERE apellido LIKE 'G%';

SELECT * FROM empleados WHERE id_departamento IS NULL;

SELECT * FROM empleados WHERE fecha_ingreso < '2022-01-01';

SELECT * FROM empleados WHERE salario BETWEEN 600000 AND 800000;
