---------------------------------------------------------------------
--
-- CAS CS 320, Fall 2015
-- Assignment 4 (skeleton code)
-- Interpret.hs
-- Written by: Navraj Narula
-- 11/16/2015

type Value = Integer
type Output = [Value]

data Term =
    Number Integer
  | Plus Term Term
  | Mult Term Term
  | Exponent Term Term
  | Max Term Term
  | Min Term Term

data Stmt =
    Print Term Stmt
  | End


--Implement the evaluate :: Term -> Value function so that 
--it evaluates abstract syntax trees of the type Term to obtain values (i.e., integers).

evaluate :: Term -> Integer
evaluate (Number n1) = n1
evaluate (Plus t1 t2) = evaluate(t1) + evaluate(t2)
evaluate (Mult t1 t2) = evaluate(t1) * evaluate(t2)
evaluate (Exponent t1 t2) = evaluate(t1) ^ evaluate(t2)
evaluate (Min t1 t2) = if evaluate(t1) < evaluate(t2) then evaluate(t1) else evaluate(t2)
evaluate (Max t1 t2) = if evaluate(t1) > evaluate(t2) then evaluate(t1) else evaluate(t2)

--Implement the execute :: Stmt -> Output function so 
--that it executes abstract syntax trees of the type Stmt to obtain an output.

execute :: Stmt -> Output
execute (Print t1 s1) = [evaluate(t1)] ++ execute(s1)
execute (End) = []



--eof