{Caso incorrecto}
{Declaracion de funciones y procedimientos.}
{Tipo de error: El identificador del tipo de la funcion no corresponde a un tipo simple.}
{Linea: 11}
{Mensaje de error: Error semantico en linea 11: El identificador arreglo1 no corresponde a un tipo simple.}
program ejemplo24;
type
	subrango1=false..true;
	arreglo1=array[subrango1] of integer;

	function f1(a:integer):arreglo1;
	begin
	{...}
	end;
begin

end.