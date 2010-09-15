{Expresiones}
{Caso incorrecto}
{Tipo de error: incompatibilidad de tipos en operacion de suma/resta.}
{Linea: 20}
{Mensaje de error: Operandos de tipos incompatibles en operacion de suma.}

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
	
	x := ((x + c) div x) * (x - z + (-y));
		
end.