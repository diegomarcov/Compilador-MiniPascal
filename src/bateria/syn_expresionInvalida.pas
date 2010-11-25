program expresioninvalida;
const c1=2;
c2=3;
type
tipo1=c1..c2;
tipo2=boolean;
tipo3= array[tipo1] of tipo2;
var a,b,c,d:integer;

procedure proc1(var a:integer;b,c,d:integer;e:tipo1);
begin
	a:=(((a+c)*b) div 10);
	if(a>0) then
		a:=b
	else
		a:=c;
end;

function func1(var a:integer;var b,c,d:integer;e:tipo1):boolean;
begin
	a:=((b+c+)*5 div e);
	if(a=b) then
		func1:=true
	else
		func1:=false;
end;

function func2(var a:integer;b:array[1..20] of boolean):boolean;
begin
	func2:=b[2];
end;

begin
a:=1;
b:=2;
c:=3;
d:=20;
proc1(a,b,c,d,25);
write(func1(a,b,c,d,5));
end.