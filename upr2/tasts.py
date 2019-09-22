
# Задача 1 - Попълнете липсващите имплементации на Human и HumanList

class Human(object):
    #write Human implementation here
    pass

class HumanList(object):
    #write HumanList implementation here
    pass



petko = Human(name='Petko', born=1995, gender='M')
assert petko.age == 23
petko.born = 1996
assert petko.age == 22

ivan1 = Human(name='Ivan', born=1989, gender='M')
stoyan = Human(name='Stoyan', born=1992, gender='M')
draganka = Human(name='Draganka', born=1997, gender='F')
ivan2 = Human(name='Ivan', born=2002, gender='M')

human_list = HumanList(
    ivan1,
    stoyan,
    draganka,
    ivan2,
)

assert human_list.humans_count == 4
assert human_list.mens_count == 3
assert human_list.womens_count == 1
assert human_list.min_age == 16
assert human_list.max_age == 29

human_list.add(petko)

assert human_list.humans_count == 5

human_list.sort_by('name', 'gender', reverse=True)
assert human_list.humans == [stoyan, petko, ivan1, ivan2, draganka]

# Задача 2: 
# Profile strenght функционалност. 
# Всеки аттрибут да има тегло релативно на останалите,
# сумата им винаги да е 100%, добавянето на нов атрибут да не налага промяна на остналите.
