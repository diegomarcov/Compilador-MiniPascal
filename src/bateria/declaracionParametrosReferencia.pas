program pr;

	var
		x:integer;
	procedure p (var a:integer;b:char);
		begin
			writeln(a);
			write(b);
		end;
	
begin
	x:=1;
	p(x,'a');
end.