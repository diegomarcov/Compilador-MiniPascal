{Expresiones}
{Caso incorrecto}
{Tipo de error: El identificador de procedimiento no forma parte de una expresion valida.}
{Linea: 22}
{Mensaje de error: Los identificadores de tipo o procedimiento no puede formar parte de una expresion.}

program ejemplo;
var
	x,y,z:integer;
	a,b,c:boolean;
	arr: array[false..true] of boolean;
	
procedure p1;
	begin
	
	end;
	
begin
	x := 1; y := 2; z := 3;
	a := true; b := true; c := false;
	
	arr[x < y] := arr[b] or p1;
		
end.