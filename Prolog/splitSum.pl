%split list A into two lists B and C where sumof(B) = sumof(C).
subsetSum(A,B,C):-
    powerset(A,B,C),
    sum(B,L),
    sum(C,R),
    L = R.
    
sum([],0).
sum(L,A):-
    sum_list_h(L,0,A).
sum_list_h([],S,S).
sum_list_h([X|Xs],S,A):-
    Sum is X+S,
    sum_list_h(Xs,Sum,A).

powerset([], [],[]).	%returns power set and the remaining set
powerset([H|T], P,[H|R]) :- powerset(T,P,R).
powerset([H|T], [H|P],R) :- powerset(T,P,R).

%to avoid answers like [1,2][3] and [3][1,2] which are the same
% leng(P,L1),
% leng([H|R],L2),
% L1=<L2
%do not make powersets past halfway point
%doesn't take care of the case where the list is even length
%subsetSum([1,2,3],[1,2],[3])


%runningSum([1,2,3,4],X). would return [1,3,6,10]
%keep partial sums so far
runningSum(X,Y):-
	run_sum_h(X,0,Y). %sum start at 0	

run_sum_h([],_,[]).
run_sum_h([X|Xs],Part,[Current|Result]):-
	Current is X + Part,
	run_sum_h(Xs,Current,Result).