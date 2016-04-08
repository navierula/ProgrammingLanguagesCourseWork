-- Navraj Narula

module Exhaustive where

import Error
import AbstractSyntax
import Parse
import TypeCheck
import Interpret
import Compile
import Machine

type Height = Integer
type Quantity = Integer

--LOOK AT NOTES ON LIST COMPREHENSIONS!!!!!!!!!!!

class Exhaustive a where
  exhaustive :: Integer -> [a]

instance Exhaustive Stmt where
  exhaustive 0 = [] 
  exhaustive x = if == 1 then [(End)] else [Print ex st | ex <- ((exhaustive (x-1)::[Exp]), st <- ((exhaustive (x-1))::[Stmt])]
  	++[Assign X ex st | ex <- ((exhaustive (x-1)):: [Exp]), s <- ((exhaustive (x-1)):: [Stmt])]
  	++[Assign Y ex st | ex <- ((exhaustive (x-1)):: [Exp]), s <- ((exhaustive (x-1)):: [Stmt])]

instance Exhaustive Exp where
  exhaustive 0 = []
  exhaustive x = if x == 1 then [(Value True), (Value False), (Variable X), (Variable Y)] else
  	[And e1 e2 | e1 <- exhaustive(x-1), e2 <- exhaustive(x-1)]
  	++[Or e1 e2 | e1 <- exhaustive(x-1), e2 <- exhaustive(x-1)]


take' :: Integer -> [a] -> [a]
take' n (x:xs) = x:(take' (n-1) xs)
take' 0 _      = []
take' _ _      = []

validate :: Height -> Quantity -> Bool
validate n k = False -- Complete for Problem 4, part (c).

complete :: String -> ErrorOr Buffer
complete _ = TypeError "Complete for Problem 4, part (d)."

--eof