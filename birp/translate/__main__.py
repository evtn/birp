from ..translated import translated as переводы
from ..argparser import аргпарсер
import os
from ..codegen_utils import БазовыйГенератор, получить_парсеры, загрузить, transform

здесь = os.path.abspath(os.path.dirname(__file__))
(
    parser,
    вычислительный_парсер,
) = получить_парсеры(os.path.join(здесь, "birp.lark"))


class Кодогенератор(БазовыйГенератор):
    вычислительный_парсер = вычислительный_парсер
    переводы = переводы


преобразователь = Кодогенератор()


def main():
    args = аргпарсер.parse_args()
    if args.переводы:
        with open(args.переводы) as file:
            переводы_пользователя = загрузить(file)

        переводы.update(переводы_пользователя)
    if args.файлы:
        try:
            import black as чёрный
        except ImportError:
            чёрный = None

        for arg in args.файлы:
            имя_ввода = arg
            with open(имя_ввода) as file:
                code = file.read()

            имя_вывода = имя_ввода.replace(".birp", ".py")
            (
                result,
                tree,
            ) = transform(code, parser, преобразователь, имя_ввода)
            if result:
                if чёрный:
                    result = чёрный.format_str(result, mode=чёрный.Mode())
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
            print("Интерактивный Борп!")
            code = input(">>> ")
            (
                result,
                tree,
            ) = transform(code, вычислительный_парсер, преобразователь, "<ввод>")
            print(f"<<< {result}")
            print(f"= {repr(eval(result))}")


if __name__ == "__main__":
    main()
