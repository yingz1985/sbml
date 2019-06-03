convert(X,Y):-	%dec to binary list
	decToBin(X,Y).

	

decToBin(0,[]):-!.
decToBin(X,P):-
	Y is X mod 2,
	Z is X \\ 2,
	decToBin(Z,R).
	append(R,[Y],P).


append([],Y,Y).
append([X|Xs],Y,[X|R]):-
	append(Xs,Y,R).
	