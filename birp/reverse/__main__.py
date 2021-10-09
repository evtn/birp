from ..translated import translated as переводы
from ..argparser import аргпарсер
import os
from ..codegen_utils import БазовыйГенератор, получить_парсеры, загрузить, transform

здесь = os.path.abspath(os.path.dirname(__file__))
(
    parser,
    вычислительный_парсер,
) = получить_парсеры(os.path.join(здесь, "birp-rev.lark"))
переводы = {value: key for key, value in переводы.items()}


class Кодогенератор(БазовыйГенератор):
    вычислительный_парсер = вычислительный_парсер
    переводы = переводы
    keys = {
        "if": "если",
        "else": "иначе",
        "elif": "иначеесли",
        "while": "пока",
        "for": "для",
        "try": "попробовать",
        "except": "кроме",
        "finally": "финально",
        "from": "из",
        "in": "в",
        "import": "подключить",
        "as": "как",
        "pass": "пропустить",
        "continue": "продолжить",
        "break": "остановить",
        "return": "вернуть",
        "def": "объявить",
        "raise": "бросить",
        "assert": "убедиться",
        "class": "класс",
        "yield": "выдать",
        "await": "ожидать",
        "async": "асинхронно",
        "lambda": "лямбда",
        "None": "Ничего",
        "True": "Да",
        "False": "Нет",
        "and": "и",
        "or": "или",
        "not": "не",
        "is": "есть",
        "del": "удалить",
        "global": "глобально",
        "nonlocal": "нелокально",
        "with": "с",
        "orig_in": "in",
        "orig_is": "is",
        "orig_not": "not",
    }


преобразователь = Кодогенератор()


def main():
    args = аргпарсер.parse_args()
    if args.переводы:
        with open(args.переводы) as file:
            переводы_пользователя = загрузить(file)

        переводы.update(переводы_пользователя)
    if args.файлы:
        for arg in args.файлы:
            имя_ввода = arg
            with open(имя_ввода) as file:
                code = file.read()

            имя_вывода = имя_ввода.replace(".py", ".birp")
            (
                result,
                tree,
            ) = transform(code, parser, преобразователь, имя_ввода)
            if result:
                if args.tree:
                    with open(имя_вывода + ".tree", "w") as file:
                        file.write(tree.pretty())

                with open(имя_вывода, "w") as file:
                    file.write(result)

                print(f"{имя_ввода} -> {имя_вывода}")
            else:
                print(f"{имя_ввода} невозможно преобразовать в {имя_вывода}")
    else:
        while True:
            print("Интерактивный Реверсивный Борп!")
            code = input(">>> ")
            result = str(
                transform(code, вычислительный_парсер, преобразователь, "<ввод>")
            )
            print(f"=> {result}")
            print(f"= {repr(eval(result))}")


if __name__ == "__main__":
    main()
