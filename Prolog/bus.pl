/*
*
*
*
*/
min_time(T):-
    times(L),
    find_min(L,T).

times(L):-
    findall(T,find_time(T),L).
find_min([X|Xs],S):-
    find_min_time(Xs,X,S). 
                  
find_min_time([],X,X). %solution is guarenteed to exist

find_min_time([H|Ts],T,S):-
    H>=T,
    find_min_time(Ts,T,S).
find_min_time([H|Ts],T,S):-
    H<T,
    find_min_time(Ts,H,S).

find_time(T):-
    find_path(P),
    calc(P,T).
    
calc([X,Y|Xs],S) :-
    M is Y-X,
    calc_trip([Y|Xs],M,S).
%take in a list of stations for our path, and calculate the time
%R for result, B for temp total, 0 initially
%X,Y for path between two stations
calc_trip([_X],R,R).

calc_trip([X,Y|T],R,B):-
    Y<X,%going back to a smaller #station
    Dist is X-Y,
    Round is 2*Dist,
    M is ((R-Dist) mod Round),
    get_Time(Round,M,P),
    A is Round - P,
    L is R+A+Dist,
    calc_trip([Y|T],L,B).
   
calc_trip([X,Y|T],R,B):-
    Y>X, %going forth to a bigger # station
    Dist is Y-X,
    Round is 2*Dist,
    M is R mod Round,
    get_Time(Round,M,P),
    A is Round - P,
    L is R+A+Dist,
    calc_trip([Y|T],L,B).
    
find_path(P):-
    last(X),
    path(0,X,P).

get_Time(X,0,X). %if result of mod is 0, it means the bus is at start

get_Time(_X,Y,Y):- %else bus is enroute 
    Y \= 0.
    
path(X,Y,P):-
    path_h(X,[Y],P).

member(X, [X|_]).
member(X, [_|Ys]) :-
    member(X,Ys).

path_h(X,[X|P], [X|P]).

path_h(A, [Y|P],R) :- 
      has_path(X,Y),   %there is a bus to y
      \+ member(X, [Y|P]), %we have not taken that bus
      path_h(A,[X,Y|P],R).  %if there's a bus to X

has_path(X,Y):-
    bus(_,X,Y); 
    bus(_,Y,X).
