program pr;

	type
		arreglo = array [boolean] of integer;

	var
		y:integer;
		x:arreglo;
	procedure p (var a:arreglo);
		begin
			a[true]:=-23;
			writeln(a[false]);
			write(a[true]);
		end;
	
begin
	x[false]:=1000;
	x[true]:=5000;
	
	p(x);
end.