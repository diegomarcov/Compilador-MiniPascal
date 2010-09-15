{Sentencia While}
{Caso incorrecto}
{Tipo de error: Expresion no booleana en sentencia while.}
{Linea: 22}
{Mensaje de error: El tipo de la expresion condicional de la sentencia while debe ser booleano.}

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
	a:= (x < y);
	a:=b;
	
	while (x div y) do
		begin
			x:=10;
			y:=10;
		end
		
		
end.