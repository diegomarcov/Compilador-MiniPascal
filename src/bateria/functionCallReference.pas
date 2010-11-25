program fun;

var
	i:integer;
function f(var z:integer;b:char):integer;
	begin
		f:=50;
		z:=54;
	end;
	
begin
	i:=12;
	write(f(i,'a'));
	write(i);
end.