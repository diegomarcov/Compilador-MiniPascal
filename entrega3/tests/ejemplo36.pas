{Caso incorrecto}
{Llamadas a funciones y procedimiento. 
Llamada a las funciones predefinidas predecesor y sucesor (enteros y booleanos)}
{Llamada a los procedimientos predefinidos write y writeln}
{Tipo de error: se trata de asignar a una variable de tipo entera el sucesor de un booleano.}
{Linea: 15}
{Mensaje de error: Error semantico en linea 15: Los tipos empleados en la asignacion son incompatibles.}
program ejemplo36;
var
a:integer;
b:boolean;

begin
a:=5;
b:=succ(a);
end.