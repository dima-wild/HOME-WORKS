#    Для онлайн-конференции необходимо написать программу, которая будет подсчитывать общую стоимость билетов. Программа должна работать следующим образом:
# 1. В начале у пользователя запрашивается количество билетов, которые он хочет приобрести на мероприятие.
# 2. Далее для каждого билета запрашивается возраст посетителя, в соответствии со значением которого выбирается стоимость:
#    Если посетителю конференции менее 18 лет, то он проходит на конференцию бесплатно.
#    От 18 до 25 лет — 990 руб.
#    От 25 лет — полная стоимость 1390 руб.
# 3. В результате программы выводится сумма к оплате. При этом, если человек регистрирует больше трёх человек на конференцию, то дополнительно получает 10% скидку на полную стоимость заказа.


num = int(input('Введите количество билетов :'))
cost = 0.0
for i in range(num):
    age = int(input('Введите возраст посетителя:'))
    if age < 18:
        cost = cost + 0
    elif 18 <= age < 25:
        cost = cost + 990
    else:
        cost = cost + 1390
if num > 3:
    cost = cost * 0.9
print('Итого:' + ' ' + str(round(cost)) + ' ' + 'рублей')