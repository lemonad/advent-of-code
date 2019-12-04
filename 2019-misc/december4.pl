% Compile with `swipl -O -g main -t halt -o bn -c december4.pl`
% Run with `./bn`
%
:- use_module(library(clpfd)) .

main :-
  aggregate_all(
      count,
      bag(U, V, W, X, Y, Z),
      (constraints(U, V, W, X, Y, Z) , part1(U, V, W, X, Y, Z)),
      N
  ) ,
  write('Number of passwords (part 1): ') , write(N) , nl ,
  aggregate_all(
       count,
       bag(G, H, I, J, K, L),
      (constraints(G, H, I, J, K, L) , part2(G, H, I, J, K, L)),
      N2
  ) ,
  write('Number of passwords (part 2): ') , write(N2) , nl .

constraints(A, B, C, D, E, F) :-
  Vs = [A, B, C, D, E, F] ,
  Vs ins 0..9 ,
  A #=< B , B #=< C , C #=< D , D #=< E , E #=< F , ! ,
  indomain(A) ,
  indomain(B) ,
  indomain(C) ,
  indomain(D) ,
  indomain(E) ,
  indomain(F) ,
  Val is (A * 100000 + B * 10000 + C * 1000 + D * 100 + E * 10 + F) ,
  Val #>= 125730 ,
  Val #=< 579381 .

part1(A, B, C, D, E, F) :-
  A #= B ; B #= C ; C #= D ; D #= E ; E #= F .

part2(A, B, C, D, E, F) :-
  (A #= B , B #\= C) ;
  (B #= C , A #\= B , C #\= D) ;
  (C #= D , B #\= C , D #\= E) ;
  (D #= E , C #\= D , E #\= F) ;
  (E #= F , D #\= E) .
