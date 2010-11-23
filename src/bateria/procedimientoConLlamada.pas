program proc;
	var a:integer;
	procedure p;
		begin
			a:=5;
		end;
begin
	a:=0;
	writeln(a);
	p;
	writeln(a);
end.