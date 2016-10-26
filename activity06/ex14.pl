secuencia(X) :- X =:= 1, write(X), nl.
secuencia(X) :- X > 1, Y is X - 1, secuencia(Y), write(X), nl.

multiplos(X, N, M) :- M is floor(N / X), !.
multiplos(X, N, M) :- X is floor(N / M), !.

digitos(X,D) :- D is floor(log10(X)) + 1.


elem_comunes(X,Y):- member(Z,X), member(Z,Y).
disjuntos(X,Y) :- \+ elem_comunes(X,Y).

posicion(X, L, N) :- \+ member(X,L), N is -1.
posicion(X, [X|_], 0).
posicion(X, [_|L], N) :- posicion(X,L,N1), !, N is N1+1.

cambia(_, _, [], []).
cambia(X, Y, [X|L], [Y|L2]) :- cambia(X, Y, L, L2), !.
cambia(X, Y, [C|L], [C|L2]) :- dif(X, C), \+ is_list(C), cambia(X, Y, L, L2), !.
cambia(X, Y, [C|L], [C2|L2]) :- cambia(X,Y,C,C2), cambia(X,Y,L,L2).