{Asignacion de arreglos}
{Caso incorrecto}
{Tipo de error: Cantidad de componentes distinta en los arreglos de la asignacion.}
{Linea: 38}
{Mensaje de error: El numero de componentes de los arreglos no puede ser distinto en una asignacion.}

program ejemplo;
var
	x,y,z:integer;
	a,b,c:boolean;
	arrInt: array[0..1] of integer;
	arrInt2: array[10..12] of integer;
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
	arrInt2[10]:=10;
	arrInt2[11]:=11;
	arrInt2[12]:=12;
	arrBool[false]:=false;
	arrBool[true]:=true;
	arrBool2[false]:=false;
	arrBool2[true]:=true;
	
	arrInt := arrInt2;
	
end.