delete(X,[],[]):- fail. %not needed, will always work

delete(X,[X|Y],Y).
delete(X,[Y|Ys],[Y|R]):-
	delete(X,Ys,R).



deleteAll(X,[],[]).
deleteAll(X,[X|Y],R):-
	deleteAll(X,Y,R).

deleteAll(X,[Y|Ys],[Y|R]):-
	X\= Y,
	deleteAll(X,Ys,R).


permute([],[]).
permute([X|Xs],Y):-
	permute(Xs,Z),
	delete(X,Y,Z).