import random

class Terrain(object):
    """docstring for Terrain"""
    def __init__(self, rows, cols, num_creatures):
        super(Terrain, self).__init__()
        self.rows = rows
        self.cols = cols
        self.cells = []
        self.creatures_map = {}
        self.day = 0
        self._deploy_cells()
        self._deploy_creatures(num_creatures)

    @property
    def creatures(self):
        creatures = []
        for cell in self.cells:
            creatures.extend(cell.creatures)
        return creatures

    @property
    def num_creatures(self):
        return len(self.creatures)

    def _deploy_cells(self):
        for row in range(self.rows):
            for col in range(self.cols):
                cell = Cell(terrain=self, row=row, col=col)
                self.cells.append(cell)

    def _deploy_creatures(self, num_creatures):
        for i in range(num_creatures):
            creature_class = random.choice([
                Scavenger,
                Herbivore,
                Carnivore
            ])
            cell = random.choice(self.cells)
            creature = creature_class(creature_id=i, cell=cell)
            self.creatures_map[creature.id] = creature

    def get_creature_by_id(self, creature_id):
        return self.creatures_map[creature_id]

    def get_cell(self, row, col):
        return next(c for c in self.cells if c.coords == (row, col))
        
    @property
    def has_alive_creatures(self):
        return any(c for c in self.creatures if c.is_alive)

    def render_status(self):
        print('----------------- DAY %s -----------' % self.day)
        for cell in self.cells:
            print('------------ CELL %s -----------' % cell)
            for creature in cell.creatures:
                print('----- {}'.format(creature))
        print('-----------------END REPORT----------------')

    def tick(self):
        self.day += 1
        for creature in self.creatures:
            if creature.is_alive:
                creature.live()


class Cell(object):
    NATURES = ['grass', 'mountain', 'water', 'desert']

    """docstring for Cell"""
    def __init__(self, terrain, row, col, nature=None):
        super(Cell, self).__init__()
        if not nature:
            nature = random.choice(self.NATURES)
        assert nature in self.NATURES
        self.row = row
        self.col = col
        self.terrain = terrain
        self.nature = nature
        self.creatures = []

    def __str__(self):
        return '<%s: %s>' % (self.coords, self.nature)

    @property
    def coords(self):
        return self.row, self.col

    @property
    def is_water(self):
        return self.nature == 'water'

    @property
    def is_grass(self):
        return self.nature == 'grass'


class Creature(object):
    class FoodError(Exception):
        pass

    STATES = ['alive', 'dead', 'eaten']
    """docstring for Creature"""
    def __init__(self, creature_id, cell):
        super(Creature, self).__init__()
        self.id = creature_id
        self.cell = cell
        self.state = 'alive'
        self.hunger = 10

    def __str__(self):
        return '<%s#%s: %s>' % (
            self.id,
            self.__class__.__name__,
            self.state.upper()
        )

    @property
    def cell(self):
        return self._cell

    @cell.setter
    def cell(self, value):
        if hasattr(self, '_cell'):
            self._cell.creatures.remove(self)
        self._cell = value
        self._cell.creatures.append(self)
        print('Creature %s is moving to: %s' % (
            self.id, self._cell
        ))
 
    @property
    def is_hungry(self):
        return self.hunger <= 5

    def eat(self):
        food = random.choice(range(0, 2))
        if not food:
            raise self.FoodError()
        self.hunger += food

    def play(self):
        self.hunger -= random.choice(range(1, 3))

    def move_to(self, cell):
        self.cell = cell

    def move(self):
        cell = random.choice(self.cell.terrain.cells)
        self.move_to(cell)

    @property
    def is_alive(self):
        return self.state == 'alive'

    @property
    def is_dead(self):
        return self.state == 'dead'

    @property
    def is_eaten(self):
        return self.state == 'eaten'

    def live(self):
        assert self.is_alive
        self.play()
        if self.is_hungry:
            try:
                self.eat()
            except self.FoodError:
                self.move()

        if self.cell.is_water:
            self.die('From water')
            return
        if self.hunger <= 0:
            self.die('From hunger')
            return
            

    def die(self, msg):
        assert self.is_alive
        self.state = 'dead'
        print('%s died: %s' % (self, msg))

    def get_killed(self, creature):
        self.die(msg='from %s' % creature)

    def get_eaten(self, creature):
        assert self.is_dead
        self.state = 'eaten'
        print('%s got eaten by: %s' % (self, creature))


class Scavenger(Creature):
    # eats animals already killed
    def eat(self):
        for creature in self.cell.creatures:
            if creature.is_dead:
                self._eat(creature)
                return
        raise self.FoodError('Nothing to eat')

    def _eat(self, creature):
        super(Scavenger, self).eat()
        creature.get_eaten(self)


class Herbivore(Creature):
    # eats grass
    def eat(self):
        if self.cell.is_grass:
            super(Herbivore, self).eat()
            return
        raise self.FoodError('No grass to eat')


class Carnivore(Creature):
    # eats alive animals (kills them)
    def eat(self):
        for creature in self.cell.creatures:
            if creature.is_alive and creature.hunger < self.hunger:
                self._eat(creature)
                return
        raise self.FoodError('Nothing to eat')

    def _eat(self, creature):
        super(Carnivore, self).eat()
        creature.get_killed(self)