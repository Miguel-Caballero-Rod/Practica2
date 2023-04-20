# Memoria Práctica 2
En esta práctica hay dos partes:

-Solución que garantiza la seguridad del sistema:

  Se divide en tres grupos (coches del norte, coches del sur y peatones), y se controla el acceso 
  de cada grupo mediante un monitor que comprueba si no hay nadie de otros grupos dentro del puente,
  es decir, hay tres variables condicion, una por cada grupo, que dan o deniegan el acceso.
  
-Solución que garantiza la ausencia de inanición:

  A parte de mantener la comporbación de que no hay nadie de los otros grupos en el puente antes de poder
  pasar, se ha creado una variable turno que funciona de la siguiente manera:
  Hay cuatro turnos posibles, uno por cada grupo, para el cual solo puede pasar gente del grupo al que
  esté vinculado, y un turno neutro, para la que pueden pasar todos.
  Se inicializa en el turno neutro, y sólo se cambiará a otro turno que no sea el neutro si hay de alguno de
  los grupos más de 5 individuos esperando. Es decir, empieza en turno neutro y empiezan a pasar del grupo A.
  Mientras pasan los del grupo A, no pueden pasar los del B ya que hay gente dentro del puente. Para evitar que
  se queden esperando eternamente, cuando haya más de 5 se fuerza la entrada de los de B, e inmediatamente cuando
  entran se vuelve a cambiar al turno neutro para que cuando pasen todos puedan entrar de otros grupos.
  Finalmente, en caso de que todos tengan a mucha gente esperando, se ha establecido un orden circular de 'paso de 
  turno' para evitar que dos grupos se 'alíen' contra otro.
