# Assignment:

Mazes
We have a maze (for example, a grid map) and mazes are placed in it. To do this, we have a group of robots whose task is to collect mazes. Each robot will take only one maze. For simplicity, we can ignore collisions between robots. Somewhere on the map is marked a collection point for mazes.

* It is possible to solve various variants, for example the positions of mazes are known in advance or not. Robots share information, or about discovered mazes, or not.
* We would like to collect as many mazes as possible in the shortest possible time. You can compete in the collection with another team of robots.

---

## Description of solution:

* Pathfinding algorithm: A-Star.
* Pyglet library was used for animations.
* Every agent runs his own A-Star algorithm.

## Visualization: 

* Red square is start position.
* Blue squeares are point of interests, that has to be collected.
* Lime squares are possible paths for agent.
* Purple squares are already found shortests paths from start to point of interest.

<img width="710" alt="image" src="https://github.com/user-attachments/assets/e0179675-836b-49c0-b681-3bfbdc975f14">




