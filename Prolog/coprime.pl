gcd(X,X,X). %gcd of same number is itself
gcd(X,Y,P):-
	X>Y,
	Z is X-Y,
	gcd(Z,Y,P).
gcd(X,Y,P):-
	X<Y,
	gcd(Y,X,P).

coprime(X,Y):-
	gcd(X,Y,1).

prime(X):-
	X=<3;
	prime_h(X,2).

prime_h(X,X). %true
prime_h(X,H):-
    X \= H,
	X mod H =\= 0,
	NewH is H + 1,
	prime_h(X,NewH).

%find two prime numbers >=2 that add to Num
goldbach(Num,A):-
    M is Num mod 2,
	M is 0, %goldbach only applies to even numbers
    E is Num -2,
	gold_h(2,E,A).

gold_h(S,E,[S,E]):-
	S =< E,
	prime(S),
	prime(E).	%cut here if we only want one answer

gold_h(S,E,A):-
    S =< E,
    N is S +1,
	M is E -1,
	gold_h(N,M,A).

%or find define all paths and get length - return if odd
evenPath(X,X). % path of length zero to itself
evenPath(X,Y):-
	edge(X,Z),
	oddPath(Z,Y).
oddPath(X,Y):-
	edge(X,Z),
	evenPath(Z,Y).