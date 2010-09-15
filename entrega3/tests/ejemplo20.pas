{Caso correcto}
{Declaracion de funciones y procedimientos.}
program ejemplo20;
const
C1=8;
var
a:integer;
type entero=integer;
     tipoBool = boolean;
     subrango1=false..true;
     subrango2=1..C1;
     arreglo1=array[subrango1] of entero;
     arreglo2=array[subrango2] of boolean;

	function f1:integer;
	var a:integer;
	begin
	{...}
	end;
	
	function f2:entero;
	begin
	{...}
	end;
	
	function f3(a:integer):subrango2;
	begin
	{...}
	end;
	
	function f4(a,b,c:integer;var d:subrango1):boolean;
	begin
	{...}
	end;
	
	procedure p1;
	begin
	{...}
	end;
	
	procedure p2(a,b:arreglo2;var c:tipoBool);
	begin
	{...}
	end;
	
	procedure p3(a,b:arreglo2;var c,d,e:integer);
	begin
	{...}
	end;
	
	procedure p4(a,b:arreglo2;var c,d,e:integer);
		function f1:integer;
		begin
		{...}
		end;
		
		function p1(var a:integer):boolean;
			procedure p4;
			begin
			{...}
			end;
		begin
		{...}
		end;
	begin
	{...}
	end;
	
begin

end.