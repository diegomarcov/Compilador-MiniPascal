program ejemplo4;
(*

EJEMPLO 4

*)
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
		
var a:integer;
var b:integer;
var c:integer;
type entero=integer;
var A: array[5] of entero;
begin
	a:=5;
	c:=0;
	b:=4;
	printEntero(sumaEnteros(a,b));
	A[2]:=sumaEnteros(a,b);
	while(c<5) do
		begin
		if(c=2) then 
			printEntero(sumaEnteros(b,c));
		else
			printEntero(sumaEnteros(a,c));
		c:=c+1;
		end;
	
end.