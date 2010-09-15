{Expresiones}
{Caso incorrecto}
{Tipo de error: Funcion con al menos un parametro formal, invocada sin parametros actuales.}
{Linea: 22}
{Mensaje de error: La funcion cuad no puede ser invocada sin parametros.}

program ejemplo;

	
var
	x,y,z:integer;
	a,b,c:boolean;
	arr: array[false..true] of boolean;
	
function cuad(a:integer):integer;
	begin
		cuad:=a*a;
	end;
	
begin
	x := 1; y := 2; z := 3;
	a := true; b := true; c := false;
	
	x:= (y div z) * cuad;

end.