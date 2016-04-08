-- Navraj Narula

module Error where

data ErrorOr a =
    Result a
  | ParseError String
  | TypeError String
  deriving Show

promote :: ErrorOr a -> ErrorOr b
promote (ParseError s     ) = ParseError s
promote (TypeError s      ) = TypeError s

instance Eq a => Eq (ErrorOr a) where
    ParseError x == ParseError y = False
    Result x == Result y = if x == y then True else False
    TypeError x == TypeError y = False

liftErr :: (a -> b) -> (ErrorOr a -> ErrorOr b)
(liftErr f) (Result x) = Result (f(x))
(liftErr f) (ParseError x) = ParseError x
(liftErr f) (TypeError x) = TypeError x

joinErr :: ErrorOr (ErrorOr a) -> ErrorOr a
joinErr (Result (Result x)) = Result x
--joinErr (ParseError x) = ParseError x
--joinErr (TypeError x) = TypeError x
joinErr (Result (ParseError x)) = ParseError x
joinErr (Result (TypeError x)) = TypeError x


--eof