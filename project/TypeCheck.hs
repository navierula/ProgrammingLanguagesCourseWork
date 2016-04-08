-- Navraj Narula

module TypeCheck where

import Error
import AbstractSyntax

type TypeEnvironment = [(Var, Type)]

typeVar :: TypeEnvironment -> Var -> ErrorOr Type
typeVar ((x,t):xvs) x' = if x == x' then Result t else typeVar xvs x'
typeVar   x' _       = TypeError (show x' ++ " is not bound.")

class Typeable a where
  check :: TypeEnvironment -> a -> ErrorOr Type

instance Typeable Stmt where
  check env (Print e s) = if check env s == Result TyVoid && check env e == Result TyBool then Result TyVoid else TypeError "ByeBye"
  check env (Assign v e s) = let env' = env ++ [(v, unwrapthis(check env e))] in if check env s == Result TyVoid && check env e == Result TyBool then Result TyVoid else TypeError "ByeBye"
  check env (End) = Result TyVoid

instance Typeable Exp where
  check env e = fold (typeVar env)(\x -> Result TyBool) 
                (\x y -> if x == Result TyBool && y == Result TyBool then Result TyBool else (TypeError "ByeBye"))
                (\x y -> if x == Result TyBool || y == Result TyBool then Result TyBool else (TypeError "ByeBye")) e

typeCheck :: Typeable a => a -> ErrorOr (a, Type)
typeCheck ast = liftErr (\t -> (ast, t)) (check [] ast) -- Pair result with its type.

-- define helper function here!!!
unwrapthis :: ErrorOr a -> a
unwrapthis (Result a) = a



--eof