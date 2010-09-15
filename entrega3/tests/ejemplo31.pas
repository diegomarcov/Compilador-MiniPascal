{Caso incorrecto}
{Llamadas a funciones y procedimiento.}
{Tipo de error: Pasaje de parametros incorrecto: se quiere pasar una constante como pametro actual y el }
{procedimiento espera un parametro por referencia}
{Linea: 21}
{Mensaje de error: Error semantico en linea 21: La expresion encontrada no corresponde a un parametro por referencia valido.}
program ejemplo27;
type 
	entero=integer;
var  
	e:entero;
	
	procedure p1(a,b:boolean;var c:integer);
	begin
{...}
	end;
	
	
begin

p1(true,true,1);

end.