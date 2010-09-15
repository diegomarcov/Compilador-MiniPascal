{Expresiones}
{Caso incorrecto}
{Tipo de error: Incompatibilidad de tipos en operacion de operador unario not.}
{Linea: 20}
{Mensaje de error: El operador unario NOT solo puede ser aplicado a un operando booleano.}

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
	
	a := ((not x) or c) and sbool;
		
end.