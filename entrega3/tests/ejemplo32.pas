{Caso incorrecto}
{Llamadas a funciones y procedimiento.}
{Tipo de error: se intenta llamar a una funcion como si fuese un procedimiento.}
{Linea: 24}
{Mensaje de error: Error semantico en linea 24: El identificador f1 no corresponde a una asignacion o llamada a procedimiento valida.}
program ejemplo32;
type 
	entero=integer;
var  
	e:entero;
	procedure p1(a,b:boolean;var c:integer);
	begin
	{...}
	end;
	
	function f1(a,b:boolean):integer;
	begin
	
	end;
	
	
begin

f1(true,false);

end.