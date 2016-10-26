papa(carlos, carolina).
papa(carlos, gabriela).
papa(olga, carlos).
papa(olga, guillermo).
papa(olga, alejandro).
papa(guillermo, xavier).
papa(guillermo, xiomara).
papa(alejandro, angelica).
papa(alejandro, alejandrita).

hijo(X, Y) :- papa(Y, X).

abuelo(X, Z) :- papa(X, Y), papa(Y, Z).

nieto(X, Z) :- hijo(X, Y), hijo(Y, Z).

hermano(X, Y) :- dif(X, Y), hijo(X, Z), hijo(Y, Z). %Built-in dif

primo(X, Y) :- papa(Z, X), papa(W, Y), hermano(Z, W).

tio(X, Y) :- hijo(Y, Z), hermano(Z, X).


xor(X, Y) :- X \= Y, !.


v(X).
b(X) :- X = 4, v(X).