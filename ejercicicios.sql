--RESPUESTA A PREGUNTA 1
select Grupo from grupo 
order by grupo asc
=============================================
--RESPUESTA A PREGUNTA 2
SELECT g.grupo, AVG(ta.Calificación) AS Promedio 
FROM `grupo` g 
right join  `tabla alumnocalificacion` ta
on g.Id_grupo  =  ta.Id_Grupo 
GROUP BY g.Grupo;
===================================================================
--RESPUESTA A PREGUNTA 3
select g.Grupo,  count(ta.Id_Grupo) as 'numero_alumnos_inscritos'
from `grupo` g right join `tabla alumnocalificacion` ta 
on g.Id_grupo  =  ta.Id_Grupo 
group by (g.Grupo)
=====================================================================
--RESPUESTA A PREGUNTA 4
select Nombre from
(
select ta.Nombre , tac.Id_Alumno , count(tac.Id_Alumno) as 'counter'
from `tabla alumno` ta 
right join `tabla alumnocalificacion` tac 
on ta.Id_Alumno  = tac.Id_Alumno
group by tac.Id_Alumno ) as counter_names
where counter >1;
========================================================================
--RESPUESTA A PREGUNTA 5
select apellido_paterno
from
(
select apellido_paterno, count(apellido_paterno) as 'counter_ap'
from `tabla alumno`
group by (apellido_paterno)) as counter_apellidos
where counter_ap >=2;
=================================================================
