{Sentencia If}
{Caso correcto}

program ejemplo;
var
	x,y,z:integer;
	a,b,c:boolean;
	sint:0..1;
	sbool:false..true;
	
begin
	x := 1; y := 2; z := 3;
	a := true; b := true; c := false;
	sint := 1;
	sbool := false;
	a:= (x < y);
	a:=b;
	
	if ((x < y) or b)
		then
			x:=10
		else
			y:=10;
		
end.