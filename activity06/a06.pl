% Determina si X es primo
primo(X) :-
	X > 1, %para cualquier número mayor que 1
	\+ (X mod 2 =:= 0), % si no es divisible entre 2
	\+ (X mod 3 =:= 0), %ni entre 3
	\+ (X mod 5 =:= 0), %ni entre 5
	\+ (X mod 7 =:= 0). %ni entre 7

primo(2). %estos son casos de primos conocidos
primo(3).
primo(5).
primo(7).


% Genera una lista Z de primos desde X hasta Y.
primos1(X,Y,Z) :-
	between(X, Y, Z), primo(Z).

primos(X,Y,Z) :-
	findall(N, primos1(X,Y,N), Z).


% Elimina duplicados consecutivos en una lista.

comprime([],[]). %caso base 1
comprime([X],[X]). %caso base 2
comprime([X,X|L1],L2) :- %si X está dos veces en la cabeza de la lista
	comprime([X|L1],L2),!. %checa en el siguiente
comprime([X,Y|L1],[X|L2]) :- %Si X y Y están en la cabeza
	dif(X,Y), %X y Y son distintos
	comprime([Y|L1],L2). %entonces comprime el resto de la lista


% Codifica longitud de las corridas de una lista

%agrupa separa en sublistas
%codifica1 es una subrutina de agrupa, que pasa de una lista a otra
%cuenta es una subrutina de codifica, y cuenta las X en [X,X,X] y lo vuelve [3,X]

%codifica es la función principal:
%primero separa en sublistas [X,X,X]
%después cuenta y lo vuelve [3,X]

agrupa([],[]). %caso base
agrupa([X|L1],[Y|L2]) :- %para la lista L1 con cabezaX, guarda en L2 con cabeza Y
	codifica1(X,L1, L3, Y), %mueve X de L1 a L3 (temporal) y guarda todo en Y
	agrupa(L3, L2). %agrupa todos los elementos iguales en L3 y guarda en L2

codifica1(X,[],[],[X]). %caso base si ya no hay elementos, entonces pasa X a una lista.
codifica1(X, [Y|L1], [Y|L1], [X]) :- %pasa X a una lista,
	dif(X, Y),!. %si X y Y son distintos
codifica1(X, [X|L1], L2, [X|L3]) :- %si aun hay elementos iguales en la cabeza de L1, pásalos a la L3
	codifica1(X, L1, L2, L3). %sigue pasando las X de la L1 a la L2, y guarda todo en L3
	
codifica(X, Y) :-
	agrupa(X,L1), %aplica agrupa a X y guarda en L1
	cuenta(L1,Y). %aplica cuenta a L1 y guarda en Y

cuenta([],[]). %caso base.
cuenta([[X|L1]|L2],[[N,X]|L3]) :- %X|L1 es una lista al principio de L2 si la lista[ N|X] está al principio de L3
	length([X|L1],N), %cuenta si la lista [X|L1] es de tamaño N
	cuenta(L2, L3). %entonces aplica cuenta a L2 y guarda en L3


%decodifica longitud de corridas de inciso d)

decodifica([],[]). %caso base
decodifica([X,L1],[X,L2]) :-
	\+ is_list(X), %si X no es una lista,
	decodifica(L1,L2), !. %decodifica L1 y guarda en L2
decodifica([[1,X]|L1],[X|L2]) :- %si la lista es [1,X] escribe X al principio de L2
	decodifica(L1,L2), !. %y decodifica el resto de L1 y guarda en L2
decodifica([[N,X]|L1],[X|L2]) :- %si la lista es [N,X], escribe X al principio de L2
	N > 1, %si N es más que 1 (hay repetición)
	N1 is N - 1, % disminuye N hasta que se vuelva 1
	decodifica([[N1,X]|L1],L2). %sigue decodificando con N1 como cabeza de L1, y guarda en L2