{Caso incorrecto}
{Llamadas a funciones y procedimiento.}
{Tipo de error: Menos cantidad de parametros actuales que formales.}
{Linea: 20}
{Mensaje de error: Error semantico en linea 20: La cantidad de parametros actuales es menor que la cantidad de parametros formales.}
program ejemplo27;
type 
	entero=integer;
var  
	e:entero;
	
	procedure p1(a,b:boolean;var c:integer);
	begin
	{...}
	end;
	
	
begin

p1(true,true);

end.