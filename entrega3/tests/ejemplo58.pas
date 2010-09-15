{Acceso a componentes de un arreglo.}
{Caso incorrecto}
{Tipo de error: Incompatibilidad de tipos en acceso a componente de arreglo.}
{Linea: 17}
{Mensaje de error: El tipo de la expresion utilizada para indexar el arreglo arr es invalido.}

program ejemplo;
var
	x,y,z:integer;
	a,b,c:boolean;
	arr: array[0..9] of boolean;
	
begin
	x := 1; y := 2; z := 3;
	a := true; b := true; c := false;
	
	arr[b] := c;
		
end.