program proc;
	type
		arreglo = array[0..2] of char;
		arreglo2 = array[0..2] of integer;
	var 
		a:arreglo;
		b:arreglo2;
	
begin	
	b[1]:=34;
	b[2]:=54;
	a:=b;
	writeln(a[0]);
	writeln(a[1]);
end.