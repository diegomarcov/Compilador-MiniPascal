{Caso incorrecto}
{Llamadas a funciones y procedimiento.}
{Tipo de error: Llamada a un procedimiento que no es visible desde el nivel lexico de la llamada.}
{Linea: 22}
{Mensaje de error: Error semantico en linea 22: El identificador p2 no se encuentra declarado. }
program ejemplo32;
type 
	entero=integer;
var  
	e:entero;
	procedure p1(a,b:boolean;var c:integer);
		procedure p2(a:integer);
		begin
		{...}
		end;
	begin
	{...}
	end;
	
	function f1(a,b:boolean):integer;
	begin
	p2(2);
	end;
	
	
begin



end.