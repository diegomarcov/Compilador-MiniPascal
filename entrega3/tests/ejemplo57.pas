{Acceso a componentes de un arreglo}
{Caso correcto}

program ejemplo;
var
	x,y,z:integer;
	a,b,c:boolean;
	sint:0..1;
	sbool:false..true;
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
	sint := 1;
	sbool := false;
	
	arrInt[7] := x + f1 * sint;
	arrInt[x - f1 div sint] := 10;
	
	arrBool[true] := x < sint;
	arrBool[(y = 3) and not(c)] := false;
	
end.