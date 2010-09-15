{Caso incorrecto}
{Llamadas a funciones y procedimiento.}
{Tipo de error: Incompatibiliad de tipos entre parametro actual y formal.}
{Linea: 20}
{Mensaje de error: Error semantico en linea 20: Incompatibilidad de tipos entre el parametro formal y el actual.}
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

p1(1,true,e);

end.