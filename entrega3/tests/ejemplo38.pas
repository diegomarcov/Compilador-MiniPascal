{Caso correcto}
{Llamadas a funciones y procedimiento. Redefinicion de las funciones sucesor y predecesor dentro de un procedimiento}

program ejemplo38;
var
a,b:integer;
	
	procedure p1;
		function succ(a:integer):integer;
			begin
			succ:=a+2;
			end;
			
		function pred(a:integer):integer;
			begin
			pred:=a-2;
			end;
	begin
	{Imprime 0 , se usa la funcion REdefinida succ}
	writeln(pred(2));
	{Imprime 10 , se usa la funcion REdefinida pred}
	writeln(succ(a));
	end;

begin
a:=8;
{Imprime 9 , se usa la funcion PREdefinida succ}
writeln(succ(a));
{Imprime 7 , se usa la funcion PREdefinida pred}
writeln(pred(a));
{Llamada a p1}
p1;
end.