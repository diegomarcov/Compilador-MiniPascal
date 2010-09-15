{Expresiones}
{Caso correcto}

program ejemplo;
var
	x,y,z:integer;
	a,b,c:boolean;
	sint:0..1;
	sbool:false..true;
	
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
	
	x := ((x + 4) div z) * (x - 3 + (-y));
	y := ((sint + (+y)) div 1) * (x + sint - f1);
	a := ((not b) or true) and sbool;
	b := ((x < y) and false) or f2;
	writeln(x);
	writeln(y);
	
end.