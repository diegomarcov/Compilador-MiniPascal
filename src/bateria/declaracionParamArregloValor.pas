program pr;

	type
		arreglo = array [boolean] of integer;

	var
		y:integer;
		x:arreglo;
	procedure p (a:arreglo);
		begin
			a[true]:=-23;
			writeln(a[false]);
			writeln(a[true]);
		end;
	
begin
	x[false]:=1000;
	x[true]:=5000;
	
	p(x);
	writeln(x[true]);
end.