-- Navraj Narula

module Interpret where

import Error
import AbstractSyntax
import TypeCheck

type ValueEnvironment = [(Var, Value)]

valueVar :: Var -> ValueEnvironment -> Value
valueVar x' ((x,v):xvs) = if x == x' then v else valueVar x' xvs

evaluate :: ValueEnvironment -> Exp -> Value
--evaluate env _ = False -- Complete for Problem 2, part (b).
--evaluate env (Variable x) = valueVar x env
--evaluate env (Value e) = e
--evaluate env (And e1 e2) = evaluate env e1 && evaluate env e2
--evaluate env (Or e1 e2) = evaluate env e1 || evaluate env e2
evaluate env ex = fold (valueVar env) (\bool -> bool) (&&) (||) ex

execute :: ValueEnvironment -> Stmt -> (ValueEnvironment, Output)
execute env (Print e s) = let (env',o) = execute env s in (env', [evaluate env e] ++ o)
execute env (Assign v e s) = let env' = env ++ [(v, evaluate env e)] in (env', snd(execute env' s))
execute env (End) = (env,[])

interpret :: Stmt -> ErrorOr Output
interpret st = if liftErr snd (typeCheck st) == Result TyVoid then Result (snd execute [] st)) else unwrapErrType (typeCheck st)

unwrapErrType :: ErrorOr a -> ErrorOr Output
unwrapErrType (TypeError a) = TypeError a

--eof


