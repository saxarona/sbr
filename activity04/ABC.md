# ABC

**Artificial Bee Colonies** use bee agents as solutions of the problem.
Depending on the evaluation of a bee, a **patch** is created around the bee position.
This patch is later populated with additional bees in order to search for new, better solutions (extra-bees).
Some other bees are used to explore other areas at random.

The algorithm was proposed by Dervis Karaboga in 2005.

> The ugly-looking pdf can be found [here][abc].

The algorithm is as follows:


    REPEAT
      1) Send the employed bees onto the food sources and determine their nectar amount.
      2) Calculate probability value of the sources with which they are preferred by the explored bees.
      3) Stop the exploitation process of the sources abandones by bees.
      4) Send the scouts into the search area for discovering new food sources, randomly.
      5) Memorize the best food source found so far.
    UNTIL(requirements are met)

Process seems easier to understand as the slides suggest:

1. Initialize `n` scout bees with a random search and evaluate their aptitude.
2. Select `m` best sites for a neighbor-search.
3. Select `e` sites for elite patches, such that `e` < `m`.
4. Select `m` - `e` sites for normal patches.
5. Determine patch-size, usually denoted as `ngh`.
6. Repeat until max_iterations:
7. Create bees for the patches:
    - `some` for elite patches
    - `some_more` for normal patches, such that `some` > `some_more`
8. Select bee with best evaluation for each patch.
9. Assign `n` - `m` bees to randomly search again.
10. Select bee with best evaluation this iteration, and GOTO 6.

[abc]: http://www-lia.deis.unibo.it/Courses/SistInt/articoli/bee-colony1.pdf