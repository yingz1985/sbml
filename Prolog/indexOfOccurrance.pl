
index(A,B,P):-
    string_to_list(A,X),
    string_to_list(B,Y),
	iterateThru(X,Y,P,0).

iterateThru([X|Xs],[Y|Ys],P,Index):-
	X is Y,
	(	localMatch(Xs,Ys),
		P is Index
    )	;
    	!,
		Next is Index + 1,
		iterateThru(Xs,[Y|Ys],P,Next).


iterateThru([X|Xs],[Y|Ys],P,Index):-
    X =\= Y,
	Next is Index + 1,
	iterateThru(Xs,[Y|Ys],P,Next).


localMatch(_,[]).
localMatch([X|Xs],[Y|Ys]):-
    X is Y,
	localMatch(Xs,Ys).

	

smallestIOC(A,B,S):-
	findall(P,index(A,B,P),[X|Y]),
	smallest_h(Y,X,S).

smallest_h([],CurrentMin,CurrentMin).

smallest_h([X|Y],CurrentMin,Result):-
	(X =< CurrentMin,
	smallest_h(Y,X,Result));
	smallest_h(Y,CurrentMin,Result).


