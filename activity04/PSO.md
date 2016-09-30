
# PSO

**Particle Swarm Optimization** is based on ducks flying.
Each duck has a **velocity**, and also remembers its **best position**.
Also, each duck has a neighborhood, and knows the **best neighborhood position**.

These three components are combined to obtain the direction which the duck shall follow.
In the end, all ducks will move near the best spot.

The code is pretty straight-forward, like most metaheuristics.
Instead of using particles, we'll be using ducks:

1. Initialize ducks
2. For each duck:
    - Calculate its evaluation
    - If its evaluation is best than his best, then update.
3. Choose duck with best evaluation as `gbest`
4. For each duck:
    - Calculate new velocity with eq. (a)
    - Calculate new position with eq. (b)
5. GOTO 2
6. Repeat `while iterations` < `max_iterations`

These are the equations in python-friendly syntax!

Eq. (a):

```python
duck.vel = c0 * duck.vel +
           c1 * rand() * (duck.pbest - duck.pos) +
           c2 * rand() * (duck.gbest - duck.pos)
```

Eq. (b):

```python
duck.pos = duck.pos + duck.vel
```