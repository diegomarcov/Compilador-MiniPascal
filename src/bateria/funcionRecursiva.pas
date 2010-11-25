Program ejemplo;
	var m: integer;
	
	function f(n:integer; k:integer) : integer;
		var p,q:integer;
		begin
		if n<2
			then 
				begin f:=n; p:=0 end
			else 
				begin
				f:= f(n-1,p)+f(n-2,q);
				p:= p+q+1
				end;
		writeln(n);
		writeln(k);
		end;
begin
write(f(3,m))
end.