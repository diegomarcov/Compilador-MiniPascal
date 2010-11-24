program fun;

type
	arr = array [0..4] of integer;
var
	a:arr;
function f(var z:arr;b:integer):integer;
	begin
		f:=50;
		b:=2;
		z[3]:=543;
		
	end;
	
begin
	a[2]:=12;
	a[3]:=-10;
	writeln(f(a,a[2]));
	writeln(a[2]);
	writeln(a[3]);
end.