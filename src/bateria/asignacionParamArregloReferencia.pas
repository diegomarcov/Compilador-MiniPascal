program pr;

	type
		arreglo = array [boolean] of integer;

	var
		y:integer;
		x:arreglo;

	procedure p (var a:arreglo);
		
		begin
			a[false]:=5;
			a[true]:=-135;
		end;
	
begin
	x[false]:=1000;
	x[true]:=5000;
	
	p(x);
	write(x[false]);
	write(x[true]);
end.