{Caso correcto}
{Factorial implementado de forma recursiva usando una funcion anidada para la multiplicacion.}
{Fibonacci implementado de forma recursiva.}
{Uso de arreglo por referencia.}
program ejemplo42;
const n=7;
type
arreglo=array[1..13] of integer;
var
a:arreglo;
func,cantidad,cont:integer;

	function Fibonacci(valor:integer):integer;
	begin
		if valor = 1 then
		fibonacci:= 1;
		if valor=0 then   fibonacci:=0;
		if valor>=2 then
		Fibonacci:=(Fibonacci(valor-1) + Fibonacci(valor-2));
	end;
	
	procedure fillArr(var a:arreglo;i,num:integer);
	{NOTA: la tercera y cuarta componentes no se cargan.}
		begin
		a[i]:=num;
		end;
		
	procedure imprArr(a:arreglo;n:integer);
	var
	i:integer;
	begin
	i:=1;
	while(i<n) do
		begin
		writeln(a[i]);
		i:=i+1;
		end;
		
	end;

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
readln(func);
cont:=1;
while(cont<=N) do
 begin
	if(func<>0) then
		fillArr(a,cont,fibonacci(cont))
	else
		fillArr(a,cont,fact(cont));
	cont:=cont+1;
 end;
 
imprArr(a,N);
end.


