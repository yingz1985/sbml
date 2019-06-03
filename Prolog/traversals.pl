node(5, 3, 6). 	%node 5 has two children, 3 and 6
node(3, 1, 4).	
leaf(1).	%leaf node
leaf(4).
leaf(6).

preorder(Root,[Root]):-
	leaf(Root). %if root is the only node

preorder(Root,[Root|R]):-	%root, lchild, rchild recursively
	node(Root,C1,C2),
	preorder(C1,R1),
	preorder(C2,R2),
	append(R1,R2,R).

append([],Y,Y).
append([X|Xs],Y,[X|R]):-
	append(Xs,Y,R).

inorder(Root,[Root]):-
	leaf(Root).

inorder(Root,R):-		%inorder works similarly to preorder
	node(Root,C1,C2),	%just need to insert root right before the right subtree
	inorder(C1,R1),
	inorder(C2,R2),
	append(R1,[Root|R2],R).

postorder(Root,[Root]):-
	leaf(Root).

postorder(Root,L):-		%do preorder and then push root at the end
	node(Root,C1,C2),
	postorder(C1,R1),
	postorder(C2,R2),
	append(R1,R2,R),
	push(Root,R,L).

push(X,[],[X]).
push(L,[X|Xs],[X|Y]):-
	push(L,Xs,Y).




