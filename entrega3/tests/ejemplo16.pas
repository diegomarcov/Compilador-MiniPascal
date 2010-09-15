{Caso correcto}
{Declaracion de variables.}
program ejemplo16;
const
C1=8;
type entero=integer;
     tipoBool = boolean;
     subrango1=false..true;
     subrango2=1..C1;
     arreglo1=array[subrango1] of entero;
     arreglo2=array[subrango2] of boolean;
var
	a,b:integer;
	c,d:subrango1;
	e:arreglo1;
	f:arreglo2;
	g:entero;
	h:boolean;
	i:tipoBool;
	j:array[1..9] of integer;
	k:array[true..true] of boolean;
	l:array[boolean] of entero;
	m:1..C1;
	n:array[subrango1] of subrango2;
	o:array[subrango1] of 1..5;
	
	procedure p1;
	var
	a:boolean;
	
	begin
	end;
begin

end.