{programa correcto - declaracion de variables, definicion de tipos, declaracion de funcion y procedimiento, pasaje de parametros
llamadas a funcion y procedimiento, expresiones}
program ejemplo1;
const c1=2;
c2=3;
type
tipo1=integer;
tipo2=boolean;
var a,b,c,d:integer;

procedure proc1(var a:integer;b,c,d:integer);
begin
	a:=(((a+c)*b) div 10);
	if(a>0) then
		a:=b
	else
		a:=c;
end;

FUNCTION func1(var a:integer;var b,c,d:integer):boolean;
begin
	a:=((b+c+d)*5);
	if(a=b) then
		func1:=true
	else
		func1:=false;
end;

begin
a:=1;
b:=2;
c:=3;
d:=20;
proc1(a,b,c,d);
write(func1(a,b,c,d));
end.