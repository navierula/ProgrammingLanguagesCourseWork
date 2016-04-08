---------------------------------------------------------------------
--
-- CAS CS 320, Fall 2015
-- Assignment 5 (skeleton code)
-- Graph.hs
-- Navraj Narula

module Graph where


data Graph a =
    Choices a (Graph a, Graph a)
  | Outcome a
  deriving (Eq, Show)

class State a where
  outcome :: a -> Bool
  choices :: a -> (a, a)


mapTuple :: (a -> b) -> (a, a) -> (b, b)
mapTuple f (a1, a2) = (f a1, f a2)
--  ... Complete for Problem #3, part (a) ...

state :: (Graph a) -> a
--  ... Complete for Problem #3, part (b) ...
state (Choices x (g1, g2)) = x
state (Outcome y) = y

instance Ord a => Ord (Graph a) where
   --(Outcome x) < (Outcome y) = x < y
   --(Choices x (a,b)) < (Choices y (f,g)) = x < y 
   --(Outcome x) <= (Outcome y) = x <= y
   g < g' = state g < state g'
   g <= g' = state g <= state g'

graph :: State a => a -> Graph a
-- init state
-- applies a function, becomes a tuple
-- this x is of type a, you're calling on choices
-- you're mapping a function
-- graph is the function I defined so I can apply it
graph x = if outcome(x) == True then Outcome x else Choices x (mapTuple graph (choices x))

depths :: Integer -> Graph a -> [Graph a] 
depths 0 (x) = [x]
depths _ (Outcome x) = [Outcome x]   
depths y (Choices x (z,t)) = (depths (y-1) z) ++ (depths (y-1) t) 

fold :: State a => (a -> b) -> (a -> (b, b) -> b) -> Graph a -> b
fold o c (Outcome x) = o x
fold o c (Choices x (g1,g2)) = c x (fold o c g1, fold o c g2)

outcomes :: State a => Graph a -> [Graph a]
outcomes g = fold (\g -> [Outcome g]) (\_(o,p) -> o++p) g





--eof