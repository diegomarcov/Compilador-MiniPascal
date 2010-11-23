program proc;
	var a:integer;
	procedure p(b:integer);
		var a:integer;
		begin
			a:=5;
			write(a);
		end;
begin
	a:=0;
	write(a);
	p(70);
	write(a);
end.