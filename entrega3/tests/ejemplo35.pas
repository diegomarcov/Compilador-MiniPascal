{Caso correcto}
{Llamadas a funciones y procedimiento. Llamada a las funciones predefinidas predecesor y sucesor (enteros y booleanos)}
{Llamadas a los procedimientos predefinidos write y writeln}
program ejemplo35;
var
b,c,d:integer;
e,f:boolean;

	procedure printBool(b:boolean);
	begin
		if(b) then
			write(1)
		else
			writeln(0);
		
	end;

	procedure pruebaEnteros;
	begin
		b:=2;
		c:=3;
		d:=succ(b);
		{Imprime 3} 
		writeln(d);
		{Imprime 4}
		writeln(succ(c));
		c:=succ(pred(b));
		{Imprime 2}
		writeln(c);
		b:=pred(pred(c));
		{Imprime 0}
		writeln(b);
	end;
	
	procedure pruebaBooleanos;
	begin
		e:=true;
		f:=succ(e);
		{Imprime 0}
		printBool(f);
		{Imprime 1}
		e:=pred(f);
		printBool(e);
	end;

begin
pruebaEnteros;
pruebaBooleanos;
end.