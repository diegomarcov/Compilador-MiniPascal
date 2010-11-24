{Caso correcto}
{Factorial implementado de forma recursiva usando una funcion anidada para la multiplicacion.}
{Fibonacci implementado de forma recursiva.}
{Uso de arreglo por referencia.}
program ejemplo42;
const n=7;

var

cont:integer;


	function fact(i:integer):integer;
		function mult(x,y:integer):integer;
			begin
			mult:=x*y;
			end;
		begin
		if(i=0) then 
			fact:=1
		else
			begin
			fact:=mult(fact(i-1),i);
			end;
		end;
		
begin

cont:=1;
while(cont<=N) do
 begin

	writeln(fact(cont));
	cont:=cont+1;
 end;
 

end.


