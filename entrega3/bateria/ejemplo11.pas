{programa incorrecto - error en linea 3, (falta el identificador del tipo de las variables)}
program ejemplo2;
var a,b:
function sumaEnteros(a:integer;var b:integer):integer;
		var c:integer;
		begin
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