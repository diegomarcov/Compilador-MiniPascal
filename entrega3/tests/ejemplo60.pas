{Caso incorrecto}
{Acceso a componentes de un arreglo.}
{Tipo de error: Acceso a una variable que no es de tipo arreglo.}
{Linea: 17}
{Mensaje de error: El identificador a no corresponde a una entidad de tipo arreglo}

program ejemplo;
var
	x,y,z:integer;
	a,b,c:boolean;
	arr: array[false..true] of boolean;
	
begin
	x := 1; y := 2; z := 3;
	a := true; b := true; c := false;
	
	arr[x < y] := arr[b] or a[true];
		
end.