import random
import pprint
from collections import OrderedDict
from itertools import chain


class Creature(object):
    class NoFoodError(Exception):
        pass

    def __init__(self, cell, number, state=1, hunger=10):
        self.number = number
        self.age = 0
        self.state = state
        self.hunger = hunger
        self.cell = cell

    def __repr__(self):
        return '<%s#%s>' % (self.__class__.__name__, self.number)

    def __str__(self):
        return '<%s#%s: %s (age: %s, hunger: %s)>' % (
            self.__class__.__name__, self.number, self.status,
            self.age, self.hunger
        )

    @property
    def status(self):
        return {
             1: 'ALIVE',
             0: 'DEAD',
            -1: 'EATEN',
        }[self.state]

    @property
    def is_alive(self):
        return self.status == 'ALIVE'

    @property
    def is_dead(self):
        return self.status == 'DEAD'
    
    @property
    def is_hungry(self):
        return self.hunger <= 4

    @property
    def position(self):
        return self.cell.position

    @property
    def terrain(self):
        return self.cell.terrain

    @property
    def cell(self):
        return self._cell
    @cell.setter
    def cell(self, value):
        assert self.is_alive, 'DEAD creatures cannot move'
        if hasattr(self, '_cell'):
            #previouts cell exists
            #remove me from there
            self._cell.creatures.remove(self)
        #set the new cell
        self._cell = value
        #add me to the new cell creatures
        self._cell.creatures.append(self)

        if self._cell.is_water:
            self.die('from water')

    def move(self):
        new_cell = random.choice(self.terrain.get_surrounding_cells(self.cell))
        print '%s moving from %s to %s' % (self, self.cell, new_cell)
        self.cell = new_cell

    def play(self):
        self.hunger -= random.choice(range(3))

    def live(self):
        assert self.is_alive, 'Only LIVE creatures can live'
        self.play()
        if self.is_hungry:
            try:
                self.eat()
            except self.NoFoodError:
                self.move()
        if not self.is_alive:
            return
        self.age += 1
        if self.hunger <= 0:
            self.die('from starving')
            return
        if self.age > 100:
            self.die('from age')
            return

    def die(self, msg):
        assert self.is_alive, 'DEAD creatures cannot die'
        self.state = 0
        print '%s died: %s' % (self, msg)

    def get_eaten(self):
        assert self.is_dead, 'Only DEAD creatures can be eaten'
        self.state = -1


class Carnivore(Creature):
    #eats alive animals
    def eat(self):
        for creature in self.cell.creatures:
            if creature.is_alive and creature is not self:
                self.kill(creature)
                return
        raise self.NoFoodError

    def kill(self, creature):
        creature.die('from %s' % self)
        self.hunger += 1
        print '%s just killed %s' % (self, creature)


class Herbivore(Creature):
    #eats grass
    def eat(self):
        if self.cell.green_food:
            self.cell.green_food -= 1
            self.hunger += 1
            return
        raise self.NoFoodError


class Scavenger(Creature):
    #eats dead animas
    def eat(self):
        for creature in self.cell.creatures:
            if creature.is_dead:
                self.ate(creature)
                return
        raise self.NoFoodError

    def ate(self, creature):
        creature.get_eaten()
        self.hunger += 1
        print '%s just ate %s' % (self, creature)


class Cell(object):
    NATURES = ['grass', 'water', 'desert', 'mountain']

    def __init__(self, terrain, position, nature):
        self._terrain = terrain
        self.position = position
        self.nature = nature
        self.green_food = 10 if nature == 'grass' else 0
        self.creatures = []

    def __repr__(self):
        return '<%s: %s>' % (self.position, self.nature)

    def __str__(self):
        return '<%s:%s>' % (self.position, self.nature)

    @property
    def terrain(self):
        return self._terrain
    
    @property
    def position(self):
        return self._position
    @position.setter
    def position(self, value):
        self._position = value
        self.terrain.cells_map[self._position] = self

    @property
    def nature(self):
        return self._nature
    @nature.setter
    def nature(self, value):
        if value not in self.NATURES:
            raise ValueError('Invalid nature %s' % value)
        self._nature = value

    @property
    def is_water(self):
        return self.nature == 'water'
    
    
class Terrain(object):
    def __init__(self, rows, cols=None):
        cols = cols or rows
        self.rows = rows
        self.cols = cols
        self.cells_map = OrderedDict()
        self.clock = 0

        self._create_cells()
        self._deploy_creatures()

    def _create_cells(self):
        for x, y in map(lambda i: divmod(i, self.cols), range(self.rows*self.cols)):
            nature = random.choice(Cell.NATURES)
            self.cells_map[x,y] = Cell(terrain=self, position=(x, y), nature=nature)

    def _deploy_creatures(self):
        for __ in range(self.rows*self.cols):
            cell = random.choice(self.cells_map.values())
            klass = random.choice([Carnivore, Herbivore, Scavenger])
            creature = klass(cell=cell, number=__)

    def get_cell(self, position):
        return self.cells_map[position]

    def get_surrounding_cells(self, cell):
        x_min = 0
        x_max = self.rows-1
        y_min = 0
        y_max = self.cols-1

        cells = []
        x, y = cell.position
        for x1 in range(x-1, x+2):
            for y1 in range(y-1, y+2):
                position = (x1, y1)
                if position == cell.position:
                    continue
                if not (x_min <= x1 <= x_max):
                    continue
                if not (y_min <= y1 <= y_max):
                    continue
                cells.append(self.get_cell(position))

        return cells

    @property
    def cells(self):
        return self.cells_map.values()

    @property
    def creatures(self):
        return list(chain(*[cell.creatures for cell in self.cells]))

    @property
    def has_alive_creatures(self):
        return any(c for c in self.creatures if c.is_alive)    

    def tick(self):
        print 'day %s is coming' % (self.clock+1)
        for creature in self.creatures:
            if creature.is_alive:
                creature.live()
        self.clock += 1

    def status(self):
        context = {}
        context['terrain'] = {
            'size': (self.rows, self.cols),
            'cells': len(self.cells_map),
            'creatures': len(self.creatures),
            'time': self.clock,
        }

        cells = []
        for cell in self.cells_map.itervalues():
            cells.append({
                '%s' % cell: cell.creatures,
            })
        context['cells'] = cells

        return context


def main():
    terrain = Terrain(2,3)
    while terrain.has_alive_creatures:
        pprint.pprint(terrain.status())
        terrain.tick()
    print 'ALL DEAD'
    pprint.pprint(terrain.status())

if __name__ == "__main__":
    main()