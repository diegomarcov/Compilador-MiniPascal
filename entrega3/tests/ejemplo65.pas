{Asignacion de arreglos}
{Caso correcto}

program ejemplo;
var
	x,y,z:integer;
	a,b,c:boolean;
	arrInt: array[0..1] of integer;
	arrInt2: array[10..11] of integer;
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
	arrBool[false]:=false;
	arrBool[true]:=true;
	arrBool2[false]:=false;
	arrBool2[true]:=true;
	
	arrInt := arrInt2;
	arrBool := arrBool2;

end.