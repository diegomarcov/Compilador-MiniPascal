{programa incorrecto - error en linea 7, (falta el begin de la funcion)}

program ejemplo2;
var a,b:integer;
function sumaEnteros(a:integer;var b:integer):integer;
		var c:integer;

			c:=a+b;
			sumaEnteros:=c;
		end;
	
	procedure printEntero(a:integer);
	begin
		write(a);
	end;
begin
	a:=5;
	b:=4;
	printEntero(sumaEnteros(a,b));
end.