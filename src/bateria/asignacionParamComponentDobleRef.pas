program pr;

	type
		arreglo = array [boolean] of integer;

	var
		y:integer;
		x:arreglo;
	procedure p2 (var a : integer);
	
		begin
			a:=-342
		end;
	procedure p (var a:integer);
		
		begin
			p2(a);
		end;
	
begin
	x[false]:=1000;
	
	
	p(x[false]);
	writeln(x[false]);
	
end.