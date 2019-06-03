quicksort([],[]). % an empty list is alredy sorted
quicksort([H|T],R):-
	partition(H,T,Ls,Rs), %partition list into lhs and rhs
	quicksort(Ls,R1),	  %sort lhs recursively
	quicksort(Rs,R2),	  %sort rhs recursively
	append(R1,[H|R2],R).

append([],Y,Y).
append([X0|X],Y,[X0|R]):-
	append(X,Y,R).

partition(Pivot,[],[],[]).

partition(Pivot,[X|L],[X|Ls],Rs):-
	Pivot =< X,
	partition(Pivot,L,Ls,Rs).


partition(Pivot,[X|L],Ls,[X|Rs]):-
	Pivot >X,
	partition(Pivot,L,Ls,Rs).



merge(L,[],L):-!.	%if only one element left, no comparison
merge([],L,L):-
    L\=[],
	!.
merge([X|Xs],[Y|Ys],[Y|R]):-
	X>Y,!,
	merge([X|Xs],Ys,R).

merge([X|Xs],[Y|Ys],[X|R]):-
	X=<Y,!,
	merge(Xs,[Y|Ys],R).

leng([],0).
leng([_X|Xs],R):-
	leng(Xs,R1),
	R is R1 + 1.
%>= and =<

takeLastN(X,0,X).	%take rest of list
takeLastN([_X|Y],Length,R):-
	Length >=0,
	M is Length -1,
	takeLastN(Y,M,R).


takeFirstN(_,0,[]).
takeFirstN([X|Y],L,[X|R]):-
	L>=0,
	M is L-1,
	takeFirstN(Y,M,R).


mergesort([X],[X]):-!.
mergesort([],[]):-!.
mergesort(L,R):-
    L = [_,_|_],	#list has at least 2 elements
	leng(L,O),
	F is O//2,
	takeFirstN(L,F,Ls),
    takeLastN(L,F,Rs),
	mergesort(Ls,R1),
	mergesort(Rs,R2),
	merge(R1,R2,R).





