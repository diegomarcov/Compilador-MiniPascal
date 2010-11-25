program pr;

	type
		arreglo = array [boolean] of integer;

	var
		y:integer;
		x:arreglo;
	procedure p2 (var a : arreglo);
	
		begin
		
		end;
	procedure p (var a:arreglo);
		
		begin
			p2(a);
		end;
	
begin
	x[false]:=1000;
	x[true]:=5000;
	
	p(x);
	write(x[false]);
	write(x[true]);
end.