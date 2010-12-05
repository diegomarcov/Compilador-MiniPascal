program pete;

function f:integer;
	procedure p;
		begin
			f:=1;
		end;
	begin
		f:=2;
		p;
	end;
	
begin
	write(f);
end.