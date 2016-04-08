---------------------------------------------------------------------
--
-- CAS CS 320, Fall 2015
-- Assignment 5 (skeleton code)
-- Algorithm.hs
-- Navraj Narula
-- NOTE: The solution to 4g is found after impatient in a comment.
-- NOTE: Extra Credit for problem 6 has been completed.
-- NOTE: Please ignore my extra notes from office hours; they're in comments.

module Algorithm where

import Graph

type Algorithm a = Graph a -> Graph a


greedy :: Ord a => Algorithm a
greedy (Outcome x) = Outcome x
greedy (Choices x (g1,g2)) = if state g1 < state g2 then g1 else g2


patient :: Ord a => Integer -> Algorithm a
--patient 0 (x) = x
--patient n (Choices x (g1,g2)) = greedy (Choices x ((patient (n-1) g1), (patient (n-1) g2)))
--patient n (Choices x (g1,g2)) = minimum (Choices x ((patient (n-1) g1), (patient (n-1) g2)))
patient n x = minimum (depths n x)


optimal :: (State a, Ord a) => Algorithm a
--optimal (Outcome x) = Outcome x
--optimal (Choices x (g1,g2)) = greedy (Choices x ((optimal g1), (optimal g2)))
optimal x = minimum (outcomes x)

metaCompose :: Algorithm a -> Algorithm a -> Algorithm a
(metaCompose g1 g2) g = g1 (g2 (g))

metaRepeat :: Integer -> Algorithm a -> Algorithm a
(metaRepeat 0 _) g = g
(metaRepeat n x) g = (metaRepeat (n-1) x (x g))

metaGreedy :: Ord a => Algorithm a -> Algorithm a -> Algorithm a
(metaGreedy x y) z = if x z < y z then (y z) else (x z)

impatient :: Ord a => Integer -> Algorithm a
impatient n g = (metaRepeat n greedy) g

--Solution to 4g:
--The patient algorithm will traverse the graph to a
--a certain depth n and return the best choice given
--the roots at that particular depth. The impatient 
--algorithm will traverse the graph either left or
--right comparing one choice against another and traverse
--down the level in which the choice is 'better.' Impatient
--can be seen as superior in the sense that its running time
--is 2*n, whereas patient's running time is n**2. In this sense,
--patent is inferior.
--Patient, on the other hand, could also be seen as superior.
--It is taking into account every choice in its comparison at a 
--certain depth. Impatient will not do this, since it traverses
--down only a certain path given each comparison. Neither algorithm
--is efficient, but patient will return a more efficient "choice,"
--noting its comparisons during the breadth-level search.


--fit :: Graph a -> [Algorithm a] -> Algorithm a
--fit g x = minimumBy 

-- Extra Notes from Office Hours:

--applies greedy n times on graph
--Impatient: impatient algorithm below is superior to patient, 
--and one way in which it is inferior.
--impatients, starts from top, among 2 children, pick the best one
--all the way linear time to a specific depth
--patient is linear
--depth first search, among all children, picks one
--impatient, best first search
--The impatient algorithm is superior to the patient algorithm
--because the patient algorithm makes recursive calls 
--The patient algorithm traverses the tree n number of times
--and chooses the best from the last depth.
--Impatient traverses the tree either left or right and runs theta(n). 
--It returns the best from the path it traverses.
--Both may not return the best optimal option.

---------------------------------------------------------------------
-- Problem #6 (extra extra credit).

-- An embedded language for algorithms.
data Alg =
    Greedy
  | Patient Integer
  | Impatient Integer
  | Optimal
  | MetaCompose Alg Alg
  | MetaRepeat Integer Alg
  | MetaGreedy Alg Alg
  deriving (Eq, Show)

interpret :: (State a, Ord a) => Alg -> Algorithm a

interpret (Greedy) = greedy
interpret (Patient x) = patient x
interpret (Impatient x) = impatient x
interpret (Optimal) = optimal
interpret (MetaCompose alg1 alg2) = metaCompose (interpret alg1) (interpret alg2)
interpret (MetaRepeat x alg) = metaRepeat x (interpret alg)
interpret (MetaGreedy alg1 alg2) = metaGreedy (interpret alg1) (interpret alg2)


data Time =
    N Integer 
  | Infinite
  deriving (Eq, Show)

instance Num Time where
  _ + Infinite = Infinite
  Infinite + _ = Infinite
  (N x) + (N y) = N(y + x)
  _ * Infinite = Infinite
  Infinite * _ = Infinite
  (N x) * (N y) = N(y * x)


performance :: Alg -> Time
performance (Greedy) = N 1
performance (Patient n) = N n^2
performance (Impatient n) = (N n) * (N 2)
performance (Optimal) = Infinite
performance (MetaCompose a1 a2) = (performance a1) + (performance a2)
performance (MetaRepeat n a) = (N n) * (performance a)
performance (MetaGreedy a1 a2) = (performance a1) + (performance a2)


--eof