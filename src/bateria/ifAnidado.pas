program ifor;

var 
	a: integer;
begin
	if 0<1 then 
		begin
			a := 1;
			if true then
				a:=a+50
		end
	else
		a := 2;
	write(a);
end.