# Activity 4

## Ant System

We saw *ACO* as an algorithm to solve **TSPs**. However, we now need it to solve **Knapsacks**, I guess. With 15^4 items. How are we doing it, then?

> A good [paper][aco] on ACO for Multi-objective knapsack.

> A whole thesis on ACOs. [Man][aco2].

> This one is actually the [bible on ACOs][acobible]

> I guess this one is the winner, [Ants can solve CSPs][acocsp]

The function we need to minimize is actually a 4-variable function, namely (in Python-friendly syntax):

````python
f = a0 / x ** 2 + a1 * math.e ** (a2 / x) + a3 math.sin(x)
sum = 0
for i in data:
	sum = sum + abs(data[i][i] - f(data[i][0], a1, a2, a3, a4, a5))
````

Where `data` is a list of (x,y) coordinates (provided).

Man, this will be haaaaard...

[aco]: http://liris.cnrs.fr/csolnon/publications/bioma04.pdf
[aco2]: http://iridia.ulb.ac.be/~mdorigo/HomePageDorigo/thesis/phd/SochaPhDThesis.pdf
[acobible]: http://www.cs.nott.ac.uk/~pszgxk/courses/g5baim/papers/ants-001.pdf
[acocsp]: http://www.cs.dartmouth.edu/~spl/Academic/AI/support/AntsCanSolveConstraintSatisfactionProblems.pdf