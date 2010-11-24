program pr;

	var
		y:integer;
	
	procedure p2 (var a : integer);
	
		begin
			a:=-342
		end;
	procedure p (var a:integer);
		
		begin
			p2(a);
		end;
	
begin
	y:=1000;
	
	
	p(y);
	writeln(y);
	
end.