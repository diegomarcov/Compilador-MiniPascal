{Asignaciones}
{Caso incorrecto}
{Tipo de error: Tipos incompatibles en la asignacion.}
{Linea: 28}
{Mensaje de error: Los tipos empleados en la asignacion son incompatibles.}

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
	
	arrBool[z = x] := 2 * f1;

end.