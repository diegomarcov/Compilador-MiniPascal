{Asignaciones}
{Caso incorrecto}
{Tipo de error: Tipos incompatibles en la asignacion.}
{Linea: 14}
{Mensaje de error: Los tipos empleados en la asignacion son incompatibles.}

program ejemplo;
var
	x,y,z:integer;
	a,b,c:boolean;
		
function f1(a:integer):boolean;
	begin
		f1:= a*a;
	end;
	
begin
	x := f1(x);

end.