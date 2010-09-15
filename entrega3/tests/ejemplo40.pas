{Caso correcto}
{Llamadas a funciones y procedimiento. Llamda a los procedimientos read y readln}

program ejemplo40;
var
a,b:integer;
begin
readln(a);
b:=a+1;
write(b);
read(b);
b:=b*4;
write(b);
end.