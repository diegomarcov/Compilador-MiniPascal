pyComp - Proyecto Final de Compiladores e Intérpretes
Comisión:
Molas, Leonardo - LU 83.815
Marcovecchio, Diego - LU 82.498

Modo de uso:	
-----------

Para ejecutar el compilador, correr en una consola:
	
	$ pyComp INPUT_FILE [OUTPUT_FILE] [-h] [-d] [-o DISPLAY_FILE],

donde:

	INPUT_FILE es el archivo con el source en Pascal
	
	OUTPUT_FILE opcionalmente indica el archivo de salida (en caso de no especificarse, se removerán los últimos tres caracteres del INPUT_FILE, y se reemplazarán por "mepa", creando un nuevo archivo con ese nombre
	
	-h muestra la ayuda de pyComp

	-d muestra el modo de debugging (realiza todas las mismas operaciones que el modo normal, pero imprime por pantalla el estado del compilador en cada paso

	-o DISPLAY_FILE hace que la salida del compilador se muestre en el archivo DISPLAY_FILE. Por defecto, DISPLAY_FILE es el archivo de salida standard del sistema operativo, por lo que de no especificarse, la salida será realizada por la pantalla.

Descripción de los casos de test:
--------------------------------

Todos los casos de test del sistema se encuentran en la carpeta /bateria.

La convención para nombrar dichos casos de test es:
	
	prefijo "wrong" indica que el caso de test es erróneo; en caso de no estar, el caso es correcto.
	prefijo "syn" indica que el caso de test dispara un error sintáctico;
	prefijo "sem" indica que el caso de test dispara un error semántico;
	prefijo "mepaError" indica que el caso de test dispara un error en tiempo de ejecución;

De esta manera, un caso de test erróneo que provoque un error semántico al realizar una asignación de variables con tipo incompatible podría llamarse, por ejemplo, "wrong_sem_AsignacionTiposIncompatibles.pas"

