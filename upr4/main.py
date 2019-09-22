from models import (
    Terrain,
    Cell,
    Scavenger,
    Herbivore,
    Carnivore
)

def main():
    terrain = Terrain(rows=4, cols=3, num_creatures=10)
    assert len(terrain.cells) == 4*3
    assert len(terrain.creatures) == 10, (
        'Terrain has %s creatures instead of 10' % len(terrain.creatures)
    )
    creature = terrain.get_creature_by_id(4)
    assert creature in creature.cell.creatures, (
        "Creature %s is not in his cell.creatures: %s" % (
            creature.id, creature.cell.creatures
        )
    )
    assert creature in terrain.creatures
    cell1 = terrain.get_cell(row=0, col=0)
    creature.move_to(cell1)
    assert creature in cell1.creatures
    cell2 = terrain.get_cell(row=0, col=1)
    creature.move_to(cell2)
    assert creature not in cell1.creatures
    assert creature in cell2.creatures

    while terrain.has_alive_creatures:
        terrain.render_status()
        terrain.tick()

        if terrain.day > 100:
            break


if __name__ == '__main__':
    main()