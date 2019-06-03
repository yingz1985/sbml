my_last(X,[X]):-!.
my_last(X,[Y,Z|Ys]):-
	my_last(X,[Z|Ys]).


kth([X|_],X,1).
kth([X|Xs],Y,I):-
	I >= 1,
	N is I-1,
	kth(Xs,Y,N).

reverse(L,R):-
	reverse_h(L,[],R). %accumulator

reverse_h([],A,A).
reverse_h([X|Xs],Acc,R):-
	reverse_h(Xs,[X|Acc],R).

palindrome(L):-
	reverse(L,L). %result of reverse = original List

flatten([],[]).	% flatten([a, [b, [c, d], e]], X). returns [a,b,c,d,e].

flatten([X|Xs],Y):-	%[ [] ] => []
	is_list(X),
	flatten(X,W),
    flatten(Xs,Z),		%[ a , [a,b,c] ] X=a Xs = [  [a,b,c] ]
    append(W,Z,Y).		%[a,b,c] => X= a , Xs= [b,c]


flatten([X|Xs],[X|Y]):-
	\+ is_list(X),	%[a,[a]] 
	flatten(Xs,Y).


%compress([a,a,a,a,b,c,c,a,a,d,e,e,e,e],X) returns [a,b,c,d,e].

compress(X,Y):-
	skip(X,Y).

skip([X],[X]).
skip([],[]).
skip([X,X|Xs],Result):-
	skip([X|Xs],Result).
skip([X,Y|Xs],[X|Result]):-
	X\=Y,	%include X if x!=y
	skip([Y|Xs],Result).

%encode([a,a,a,a,b,c,c,a,a,d,e,e,e,e],X). returns [(4,a),(1,b)]
encode(X,Y):-
	encode_h(X,0,Y).	

encode_h([X],Acc,[(A,X)]):-
	A is Acc + 1.
encode_h([],_,[]).
encode_h([X,X|Xs],A,Result):-
	C is A + 1,
	encode_h([X|Xs],C,Result).
encode_h([X,Y|Xs],A,[(C,X)|Result]):-
	X\=Y,	%include X if x!=y
    C is A + 1,
	encode_h([Y|Xs],0,Result).

%I could also do pack but I'm lazy..

%double every occurrance of something


duple([],[]).
duple([X|Y],[X,X|R]):-
	duple(Y,R).

%call flatten if necessary
%variable number of repetitions per element
dupli([X|Xs],L,[R1|R]):-
	repeatN(X,L,R1),
	dupli(Xs,L,R).

dupli([],_,[]).

repeatN(_,0,[]):-!.
repeatN(X,L,[X|R]):-
	M is L-1,
	repeatN(X,M,R).

append([],L,L).
append([H|T],L,[H,T2]):-
	append(T,L,T2).


interleave(X,[],X).
interleave([],Y,Y).
interleave([X|Xs],[Y|Ys],[X|R]):-
	interleave(Xs,[Y|Ys],R).
interleave([X|Xs],[Y|Ys],[Y|R]):-
	interleave([X|Xs],Ys,R).

interleaveAll(L1,L2,L):
	findall(C,interleave(L1,L2,C),L).


powerset([],[]).
powerset([H|T],[H|R]):-
	powerset(T,R).
powerset([_|T],R):-
	powerset(T,R).

delete(_,[],[]):-fail.	%should have something to delete
delete(X,[X|Y],Y).
delete(X,[Y|Ys],[Y|R]):-
	delete(X,Ys,R).

permute([],[]).
permute([X|Y],Z):-
	permute(Y,W),
	delete(X,Z,W).


member(X,[X|_]).
member(X,[Y|Xs]):-
	Y\=X,
	member(X,Xs).

%graph problems

%test if a graph is reflexive, (anti)symmetric, and transitive
%A = a list of graph vertices
%G = graph in list of edges form

refiexive([],_). %an empty graph is reflexive 
reflexive([H|T],G):-	%for every vertex there is an edge(V,V) in graph
	member(edge(H,H),G),
	reflexive(T,G).


symmetric(_A,G):-	%symmetric if for every edge X,Y there exists Y,X
	symmetric_h(G,G).	%list of vertices is not relevent
						%since not every vertex is connected to each other
symmetric_h([edge(X,Y)|P],G):-
	member(edge,Y,X,G),
	symmetric_h(P,G).

transitive(_A,G):-	%transitive if for (a,b) (b,c) then (a,c)
	\+ non_transitive(G).

non_transitive(G):-
	member(edge(X,Y),G),
	member(edge(Y,Z),G),
	\+ member(edge(X,Z),G).

anti_symmetric(A,G):-	%if there's an edge X,Y and Y,X then X=Y
	\+ non_anti_symmetric(G).

non_anti_symmetric(G):-	%if there is any edge such that it's symmetric
	member(edge(X,Y),G),
	member(edge(Y,X),G),
	Y \= X.

cartesian_product([],_,[]).
cartesian_product(_,[],[]).
cartesian_product([X|Y],L2,R):-
	pair(X,L2,R1),
	cartesian_product(Y,L2,R3),
	append(R1,R3,R).





pair(X,[],[]).
pair(X,[Y|Ys],[(X,Y)|R]):-
	pair(X,Ys,R).


%returns a list of prime numbers in range X-Y

r_prime(X,Y,Z):-
    range_prime_h(X,Y,Z).

range_prime_h(X,Y,[]):-
	X>Y,
    !.
range_prime_h(X,Y,[X|R]):-
    X=<Y,
    prime(X),
    Z is X + 1,
    range_prime_h(Z,Y,R),!.
range_prime_h(X,Y,R):-
    X=<Y,
    \+prime(X),
    Z is X+1,
    range_prime_h(Z,Y,R).

%determine path from X to some destination

path(X,[X|Y],[X|Y]). %arrived at dest
path(X,[Y|P],Z):-
    edge(X,Y),
    \+ member(X,[Y|P]),
    path(X,[X,Y|P],Z).

cycle(A,P):-
	edge(A,B), %there's at least an edge from A to elsewhere
	path(B,A,Z), %find all the paths from B-A
	P is [A|Z].


find_all_terms(_,[],[]).
find_all_terms(X,[X|Ys],[X|P]):-
	find_all_terms(X,Ys,P).
find_all_terms(X,[Y|Ys],P):-
	X\=Y,
	find_all_terms(X,Ys,P).










	






























