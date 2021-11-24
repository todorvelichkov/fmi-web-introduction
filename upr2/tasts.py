
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

# Задача 2: Profile strenght
# Функционалност: 
#   Всеки аттрибут да има тегло релативно на останалите,
#   сумата им винаги да е 100%, добавянето на нов атрибут да не налага промяна на остналите.

# Задача 3: Stopwatch
# Функционалност:
#   Хронометър, който да има следните методи: start, stop, pause, reset, save_time, show_time, saved_times

# Задача 4: Вендинг машина
# Функционалност:
#   1) При зададени типове банкноти (1,2,5,10,20,50) изчисли как с най-малко банкноти да се върне определено ресто
#   2) При заредени определени банкноти, намери с кои банкноти да се върне ресто.

