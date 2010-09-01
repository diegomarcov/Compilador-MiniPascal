program ejemplo3;
{Declaracion de tipo entero}
type entero=integer;
var A: array[5] of entero;
var a:entero;
(**********************)
(*Comienzo del programa*)
(**********************)
begin
a:=100;
(* Asigno a la componenete 2 del arreglo el valor de a (de tipo entero)*)
A[2]:=a;

end.