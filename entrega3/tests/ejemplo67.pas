{Asignacion de arreglos}
{Caso incorrecto}
{Tipo de error: Tipos indice incompatibles en los arreglos de la asignacion.}
{Linea: 37}
{Mensaje de error: Los tipos indice de los arreglos no pueden ser incompatibles en una asignacion.}

program ejemplo;
var
	x,y,z:integer;
	a,b,c:boolean;
	arrInt: array[0..1] of integer;
	arrInt2: array[boolean] of integer;
	arrBool: array[false..true] of boolean;
	arrBool2: array[boolean] of boolean;
	
function f1:integer;
	begin
		f1:=2;
	end;

function f2:boolean;
	begin
		f2:=true;
	end;	
	
begin

	arrInt[0]:=0;
	arrInt[1]:=1;
	arrInt2[false]:=10;
	arrInt2[true]:=11;
	arrBool[false]:=false;
	arrBool[true]:=true;
	arrBool2[false]:=false;
	arrBool2[true]:=true;
	
	arrInt := arrInt2;
	
end.