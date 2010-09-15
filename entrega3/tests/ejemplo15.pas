{Caso incorrecto}
{Declaracion de tipos: arreglos.}
{Tipo de error: El tipo componente del arreglo no es un tipo simple.}
{Linea: 10}
{Mensaje de error: Error semantico en linea 10: El tipo componente de un arreglo debe ser un tipo simple.}
program ejemplo15;

type 
     arreglo1=array[1..2] of boolean;
     arreglo2=array[boolean] of arreglo1;

     
begin

end.