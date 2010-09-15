{Caso correcto}
{Llamadas a funciones y procedimiento. Redefinicion de los procedimientos write y writeln dentro de un procedimiento}

program ejemplo39;
var
a:integer;
	
	procedure p1(var a:integer);
	var
	b,c:integer;
		procedure write(var b:integer);
			begin
			b:=b+5;
			end;
			
		procedure writeln(var c:integer);
			begin
			c:=c+2;
			end;
	begin
	b:=2;
	c:=3;
	write(b);
	writeln(c);
	{El parametro por referencia a toma el valor 13}
	a:=a+b+c;
	end;

begin
a:=1;
p1(a);
{Imprime 13}
writeln(a);
end.