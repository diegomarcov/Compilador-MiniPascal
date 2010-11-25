program pr;

	var
		y:char;
		
	procedure p (var a:char);
		begin
			a:='5';
			
		end;
	
begin
	y:='a';
	
	p(y,5);
	write(y);
end.