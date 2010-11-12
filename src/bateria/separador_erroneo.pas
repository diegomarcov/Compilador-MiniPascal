program separador_erroneo;
type entero=integer;
var A: array[boolean] of entero;

	function sumaEnteros(a:integer;var b:integer):integer;
		var c:integer;
		begin
			
		end;
	
	procedure printEntero(a:integer);
	begin
		write(a);
	end;
begin
	a:=5;
	c:=0;
	b:=4;
	printEntero(sumaEnteros(a,b));
	A[2]:=sumaEnteros(a,b);
	if(c=2) then 
		printEntero(sumaEnteros(b,c));
	else
		printEntero(sumaEnteros(a,c));
	c:=c+1;
end.