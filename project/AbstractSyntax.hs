-- Navraj Narula

module AbstractSyntax where

type Value = Bool
type Output = [Value]

data Var = X | Y deriving Eq

instance Show Var where
  show X = "x"
  show Y = "y"

data Stmt =
    Print Exp Stmt
  | Assign Var Exp Stmt
  | End
  deriving (Eq, Show)

data Exp =
    Variable Var
  | Value Bool
  | And Exp Exp
  | Or Exp Exp
  deriving (Eq, Show)

data Type =
    TyBool
  | TyVoid
  deriving (Eq, Show)

--Complete for Problem 1, part (c).

fold :: (Var -> b) -> (Bool -> b) -> (b -> b -> b) -> (b -> b -> b) -> Exp -> b
fold v b a o (Variable x) = v(x)
fold v b a o (Value x) = b(x)
fold v b a o (And x y) = a (fold v b a o x) (fold v b a o y) 
fold v b a o (Or x y) = o (fold v b a o x) (fold v b a o y) 

--foldStmt :: (Exp -> b -> b) -> (Var -> Exp -> b -> b) -> b -> Stmt -> b
--foldStmt x y z (Print e s) = x (foldStmt x y z e) (foldStmt x y z s) 
--foldStmt x y z (Assign v e s) = y (foldstmt x y z v) (foldStmt x y z e) (foldStmt x y z s)
--foldStmt x y z (End) = z

--Complete for Problem 1, part (c).
size :: Exp -> Integer
size s = fold (\s -> 1) (\s -> 1) (\v y -> v + y + 1) (\v y -> v + y + 1) s


--eof