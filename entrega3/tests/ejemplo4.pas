{Caso correcto}
{Declaracion de tipos: identidad, subrango ,arreglos}
program ejemplo4;
const
C1=2;
C2=true;
C3=C2;
C4=C1;
C5=-3;
type entero=integer;
     integer=boolean;
     subrango1=false..true;
     subrango2=false..false;
     subrango3=true..true;
     subrango4=0..1;
     subrango5=-5..-1;
     subrango6=1..C1;
     subrango7=C5..C1;
     
     arreglo=array[1..9] of entero;
     arreglo1=array[boolean] of boolean;
     arreglo2=array[C5..C1] of boolean;
     arreglo3=array[1..C1] of entero;
     arreglo4=array[false..true] of integer;
     arreglo5=array[boolean] of integer;
     arreglo6=array[true..true] of boolean;
     arreglo7=array[false..false] of boolean;
     arreglo8=array[subrango1] of boolean;
     arreglo9=array[subrango2] of entero;
     arreglo10=array[subrango3] of subrango1;
     arreglo11=array[subrango4] of subrango2;
     arreglo12=array[subrango5] of boolean;
     arreglo13=array[subrango6] of boolean;
     arreglo14=array[boolean] of -9..-C1;
     

begin

end.