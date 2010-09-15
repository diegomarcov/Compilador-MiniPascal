{Caso incorrecto}
{Llamadas a funciones y procedimiento.}
{Tipo de error: Mayor cantidad de parametros actuales que formales.}
{Linea: 20}
{Mensaje de error: }
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

p1(true,true,e,d);

end.