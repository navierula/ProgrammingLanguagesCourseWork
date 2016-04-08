-- Navraj Narula

module Compile where

import Error
import AbstractSyntax
import TypeCheck
import Machine

convert :: Value -> Integer
convert True = 1
convert False = 0

converts :: Output -> Buffer
converts os = map convert os 

type AddressEnvironment = [(Var, Address)]

addressVar :: Var -> AddressEnvironment -> Address
addressVar x' ((x,a):xas) = if x == x' then a else addressVar x' xas

class Compilable a where
  compile :: AddressEnvironment -> a -> [Instruction]

instance Compilable Exp where
  -- USE NOTES EXAMPLE, SET 4 10!!!!!!
  compile env (Variable X) = [SET 3(addressVar X env), SET 4 12, COPY]
  compile env (Variable Y) = [SET 3(addressVar Y env), SET 4 12, COPY]
  compile env (Value True) = [SET 12 1]
  compile env (Value False) = [SET 12 0]
  -- Try to do 'and' with size if you have time
  -- Look at Lapets' simulator and construct AND
  compile env (And e1 e2) = (compile env e1) ++ [SET 3 12, SET 4 1, COPY] ++ (compile env e2) ++ [SET 3 12, SET 4 2, COPY, MUL, SET 3 0, SET 4 7, COPY]
  -- Use OR with size!!!!!
  compile env (Or e1 e2) = compile env (Or e1 e2) ++ compile env e1 ++ [SET 3 (size e1 + 8), SET 4 1] ++ compile env e2 ++ [SET 3 (size e2 + 8), SET 4 2, COPY, ADD, SET 3 0, SET 4 (size (Or e1 e2) + 8), COPY]

instance Compilable Stmt where
  compile env (End) = []
  compile env (Assign X ex st) = (compile env ex) ++ [SET 3 2, SET 4 11, COPY] ++ (compile env st)
  compile env (Assign Y ex st) = (compile env ex) ++ [SET 3 2, SET 4 11, COPY] ++ (compile env st)
  compile env (Print ex st) = (compile env ex) ++ [SET 3 2, SET 4 5, COPY] ++ (compile env st)
  
compileSimulate  :: Stmt -> ErrorOr Buffer
-- Go back to Error, what can you lift here????
compileSimulate st = if liftErr snd (typeCheck st) == Result TyVoid then Result (simulate(compile [] st)) else typeErrUnwrap (typeCheck st)

typeErrUnwrap :: ErrorOr a -> ErrorOr Buffer
-- Define separate helper function to upwrap appropriately!!!!!!
typeErrUnwrap (TypeError a) = TypeError a


--eof