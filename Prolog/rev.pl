reverse([],[]).
reverse([X|Y],A):-
	reverse(Y,Z),
	append(Z,[X],A).


append([],Y,Y).
append([X|Y],Ys,[X|R]):-
	append(Y,Ys,R).


rev(L1, L2) :- 
	rev_h(L1, [], L2).
	
rev_h([X|Xs], AccBefore, Out):-
	rev_h(Xs, [X|AccBefore], Out).

rev_h([], Acc, Acc).