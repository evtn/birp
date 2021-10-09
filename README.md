# birp (борп) - большой русский питон

Почему большой? [Потому что](https://ru.wikipedia.org/wiki/%D0%91%D0%BE%D0%BB%D1%8C%D1%88%D0%BE%D0%B9_%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9_%D0%BA%D0%BE%D1%82).    
Почему русский? Потому что на русском.    
Почему питон? [Потому что](https://ru.wikipedia.org/wiki/Python).    

## Что?

С помощью данного модуля вы сможете писать код на русском, но всё ещё пользоваться всеми преимуществами Питона! (пожалуйста, не надо)    
Транслятор переводит не только ключевые слова, но и встроенные функции, типы, магические методы, а так же некоторые другие слова 

Пример кода:
```
граница = целое(ввод("Введите верхнюю границу: "))

для число в диапазон(граница):
    вывод(число)
```

Пример транслируется в:

```python
bound = int(input("Введите верхнюю границу: "))

for number in range(bound):
    print(number)
```

Транслятор Борп в том числе написан на Борп (см. файлы \*.birp в репозитории)

## Установка

`python -m pip install birp`

## Использование

Напишите ваш код в файле с расширением .birp и запустите простую команду:

`python -m birp -f файл1 файл2...`

Более подробно об использовании аргументов расскажет `python -m birp -h`

## Документация

Когда-нибудь - обязательно. Пока смотрите примеры (папка `examples`) и используйте обратную трансляцию (см. ниже)

## Обратная трансляция
Для тех, кому очень лениво переписывать тысячи строчек кода, сделан модуль обратной трансляции (из обычного Питона в Борп):

`python -m birp.reverse -f файл1 файл2...`

### Очень хороший пример обратной трансляции

```
git clone https://github.com/keon/algorithms
python -m birp.reverse -f algorithms/algorithms/*/*.py
```