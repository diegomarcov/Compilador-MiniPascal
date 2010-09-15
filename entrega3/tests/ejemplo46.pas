{Expresiones}
{Caso incorrecto}
{Tipo de error: incompatibilidad de tipos en operacion de operador unario +.}
{Linea: 20}
{Mensaje de error: El operador unario "+" solo puede ser aplicado a un operando entero.}

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
	
	x := ((x + y) div x) * (x - z + (+c));
		
end.