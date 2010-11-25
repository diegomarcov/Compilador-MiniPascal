program util;
var
	a : boolean;
begin
	a:=true;
	while a do
		begin
			while false do
				a:=true;
			a:=false;
		end;
end.