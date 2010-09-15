{Asignaciones}
{Caso correcto}

program ejemplo;
var
	x,y,z:integer;
	a,b,c:boolean;
	arrInt: array[0..9] of integer;
	arrBool: array[false..true] of boolean;
	
function f1:integer;
	begin
		f1:=2;
	end;

function f2:boolean;
	begin
		f2:=true;
	end;	
	
begin
	x := 1; y := 2; z := 3;
	a := true; b := true; c := false;
	
	x := ((x + 4) div z) * (arrInt[4]);
	y := (x + arrInt[x*y] - f1);
	arrBool[true] := ((not b) or true) and f2;
	arrBool[z = x] := ((x < y) and false) or f2;

end.