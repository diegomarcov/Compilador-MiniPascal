program pr;

	type
		arreglo = array [boolean] of integer;

	var
		y:integer;
		x:arreglo;
	procedure p (a:integer);
		begin
			writeln(a);
			a:=-23;
			writeln(a);
			
		end;
	
begin
	x[false]:=1000;
	x[true]:=5000;
	
	p(x[false]);
	writeln(x[false]);
end.