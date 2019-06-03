member(X, [X|_]).
member(X,[_,|Y]):- 
	member(X,Y);

append([],L.L);
append([H|T],L,[H,T2]):-
	append(T,L,T2);

max(X,Y,Y) :-
	X =< Y.

max(X,Y,X) :-
	X>Y.


#! cut exeution on branching

my_last([],0).
my_last([H],H).
#my_last([H],H):- !. if cut succeeded, stop executing 
my_last([_H,H2|T],X) :-
	my_last([H2|T],X]).

#[1] can go into both my_last with one element, if my_last([H|T],X) since [1] is list with empty T
#will return 1 and 0, but 0 is incorrect 


my_kth([],_,0).
my_kth([H|T],0,H).
my_kth([H|T],N,X):-
	N\=0,
	N2 is N-1,
	my_kth(T,N2,X).

reverse([],[]).
reverse([H|T],R) :- reverse(T,RT),append(RT,[H],R).

my_flatten(X,[X]) :- \+ is_list(X).
my_flatten([],[]).
my_flatten([X|Xs],Zs)


