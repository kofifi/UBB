#const n = 6.

block(a;b;c;d;e).
place(X) :- block(X).
place(table).
step(1..n).

on(b,table,0). on(c,table,0).
on(e,table,0). on(a,e,0). on(d,a,0).

goal(a,table). goal(b,a). goal(c,b). goal(d,c). goal(e,d).

{ move(B,P,T) : block(B), place(P), B != P } = 1 :- step(T).

:- move(B,_,T), on(_,B,T-1).
:- move(_,P,T), block(P), on(_,P,T-1).
:- move(B,P,T), on(B,P,T-1).

moved(B,T) :- move(B,_,T).
on(B,P,T) :- move(B,P,T).
on(B,P,T) :- on(B,P,T-1), step(T), not moved(B,T).

:- goal(B,P), not on(B,P,n).

#show move/3.
