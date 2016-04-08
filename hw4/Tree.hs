---------------------------------------------------------------------
--
-- CAS CS 320, Fall 2015
-- Assignment 4 (skeleton code)
-- Tree.hs
-- Written by: Navraj Narula
-- 11/16/2015

data Tree =
    Leaf
  | Twig
  | Branch Tree Tree Tree
  deriving (Eq,Show);

--Implement a function twigs :: Tree -> Integer that 
--returns an integer representing the total number of Twig values in the input tree.
twigs :: Tree -> Integer

twigs(Twig) = 1
twigs(Leaf) = 0
twigs(Branch t1 t2 t3) = twigs(t1) + twigs(t2) + twigs(t3)


--Implement a function branches :: Tree -> Integer that 
--returns an integer representing the total number of branches in the input tree.
branches :: Tree -> Integer

branches(Twig) = 0
branches(Leaf) = 0
branches (Branch t1 t2 t3) = 1 + branches(t1) + branches(t2) + branches(t3)

--Implement a function width :: Tree -> Integer that returns an integer representing the 
--width of the input tree. Trees consisting of a Leaf or Twig are defined to have a
-- width of 1; all other trees are as wide as the sum of the widths of their children.
width :: Tree -> Integer

width(Leaf) = 1
width(Twig) = 1
width(Branch t1 t2 t3) = width(t1) + width(t2) + width(t3)


--A tree is perfect if all the leaves of the tree are at the same depth and it has no twigs. 
--Define a function perfect :: Tree -> Bool that returns True if the 
--input tree is perfect and False otherwise.
perfect :: Tree -> Bool

perfect(Leaf) = False
perfect(Twig) = False
perfect(Branch Leaf Leaf Leaf) = True
perfect(Branch t1 t2 t3) = perfect(t1) && perfect(t2) && perfect(t3)



--A tree is degenerate if all the branches are part of a single path. 
--Equivalently, a tree is degenerate if all nodes have at least two non-node children. 
--Define a function degenerate :: Tree -> Bool that returns True if the tree supplied
--is degenerate, and False otherwise.
degenerate :: Tree -> Bool

degenerate(Twig) = True
degenerate(Leaf) = True

degenerate(Branch t1 Leaf Leaf) = True && degenerate(t1)
degenerate(Branch t1 Leaf Twig) = True && degenerate(t1)
degenerate(Branch t1 Twig Leaf) = True && degenerate(t1)
degenerate(Branch t1 Twig Twig) = True && degenerate(t1)


degenerate(Branch Leaf t1 Leaf) = True && degenerate(t1)
degenerate(Branch Leaf t1 Twig) = True && degenerate(t1)
degenerate(Branch Twig t1 Leaf) = True && degenerate(t1)
degenerate(Branch Twig t1 Twig) = True && degenerate(t1)

degenerate(Branch Leaf Leaf t1) = True && degenerate(t1) 
degenerate(Branch Leaf Twig t1) = True && degenerate(t1)
degenerate(Branch Twig Leaf t1) = True && degenerate(t1)
degenerate(Branch Twig Twig t1) = True && degenerate(t1)

degenerate(Branch t1 t2 t3) = False

--Define a tree infinite :: Tree that is infinitely large, 
--but in which every branch has a left Leaf child, a right Leaf child, and a Branch middle child.
infinite :: Tree 

infinite = Branch Leaf infinite Leaf


--eof