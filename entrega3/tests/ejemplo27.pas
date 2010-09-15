{Caso correcto}
{Llamadas a funciones y procedimiento.}

program ejemplo27;
type entero=integer;
     tipoBool = boolean;

     arreglo1=array[1..6] of entero;
     arreglo2=array[2..7] of integer;
    
var
	a:arreglo1;
	b:arreglo2;
	c:tipoBool;
	d:integer;
	e:entero;
	
	procedure p1(a,b:boolean;var c:integer);
	begin
	{...}
	end;
	
	procedure p2(a:arreglo1;b:arreglo2);
	begin
	{...}
	end;
	
	function f1:boolean;
	begin
	{...}
	p2(a,b);
	{...}
	end;
	
	function f2(a:arreglo1;var b:integer):boolean;
		procedure p3(b:integer);
		begin
		{...}
		end;
	begin
	p3(b);
	end;
	
	
	procedure p3(a:arreglo1;b:arreglo2);
		procedure p4(a:arreglo1;b:arreglo2);
		begin
		{...}
		end;
	begin
	p4(a,b);
	end;
	
begin

p1(true,true,e);
p2(b,a);
p1(f1,f2(a,d),e);
end.