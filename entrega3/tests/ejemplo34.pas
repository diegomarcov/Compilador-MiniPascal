{Caso incorrecto}
{Llamadas a funciones y procedimiento.}
{Tipo de error: Llamada a una subrutina declarada mas abajo.}
{Linea: 14}
{Mensaje de error: Error semantico en linea 14: El identificador p2 no se encuentra declarado.}
program ejemplo32;
type 
	entero=integer;
var  
	e:entero;

	function f1(a,b:boolean):integer;
	begin
	p2(2);
	end;
	
	procedure p1(a,b:boolean;var c:integer);
		procedure p2(a:integer);
		begin
{...}
		end;
	begin
{...}
	end;
	
	
begin



end.