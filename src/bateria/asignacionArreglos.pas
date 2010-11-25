program ej3;
type
	arreglo = array [0..1] of integer;
var 
	a : arreglo;
	b : arreglo;
begin
	a[0]:=11;
	a[1]:=38;
	writeln(a[0]);
	writeln(a[1]);
	b:=a;
	writeln(b[0]);
	writeln(b[1]);
end.