from lark import (
    Lark as Жаворонок,
    Transformer as Преобразователь,
    UnexpectedToken as НепредвиденныйТокен,
    UnexpectedCharacters as НепредвиденныеСимволы,
    UnexpectedEOF as НепредвиденныйКФ,
)
from lark.indenter import Indenter as Отступник
from json import load as загрузить
from traceback import format_exc


class ОтступникПитона(Отступник):
    NL_type = "_NEWLINE"
    OPEN_PAREN_types = ["LPAR", "LSQB", "LBRACE"]
    CLOSE_PAREN_types = ["RPAR", "RSQB", "RBRACE"]
    INDENT_type = "_INDENT"
    DEDENT_type = "_DEDENT"
    tab_len = 8


символ_отступа: str = "    "


def добавить_отступ(text: str) -> str:
    if text.strip():
        return text.replace("\n", "\n" + символ_отступа)
    return ""


def с_пробелом(text):
    return " ".join(["", text])


def пропустить_пустые(tokens):
    return filter(None, tokens)


def проверка_интерполяции(token, курсор):
    вложенность = 0
    for смещение in range(курсор, len(token)):
        if token[смещение] == "{":
            вложенность += 1
        elif token[смещение] == "}":
            вложенность -= 1
        if вложенность < 0:
            return смещение
    else:
        raise ValueError("Неверная интерполяция")


def получить_парсеры(файл_грамматики):
    with open(файл_грамматики) as file:
        грамматика = file.read()

    args = dict(parser="lalr", postlex=ОтступникПитона(), maybe_placeholders=True)
    parser = Жаворонок(грамматика, start="file_input", **args)
    вычислительный_парсер = Жаворонок(грамматика, start="eval_input", **args)
    return parser, вычислительный_парсер


class БазовыйГенератор(Преобразователь):
    keys = {
        "if": "if",
        "else": "else",
        "elif": "elif",
        "while": "while",
        "for": "for",
        "try": "try",
        "except": "except",
        "finally": "finally",
        "from": "from",
        "in": "in",
        "import": "import",
        "as": "as",
        "pass": "pass",
        "continue": "continue",
        "break": "break",
        "return": "return",
        "def": "def",
        "raise": "raise",
        "assert": "assert",
        "class": "class",
        "yield": "yield",
        "await": "await",
        "async": "async",
        "lambda": "lambda",
        "None": "None",
        "True": "True",
        "False": "False",
        "and": "and",
        "or": "or",
        "not": "not",
        "is": "is",
        "del": "del",
        "global": "global",
        "nonlocal": "nonlocal",
        "with": "with",
        "orig_in": "в",
        "orig_is": "есть",
        "orig_not": "не",
    }

    def file_input(self, tokens):
        return "\n".join(tokens)

    def eval_input(self, tokens):
        return tokens[0]

    def __getattr__(self, attr):
        if attr.isupper():
            return lambda token: token
        print(f"!!! {attr} не преобразован !!!")
        return lambda tokens: " ".join(tokens)

    def one_line_suite(self, tokens):
        return tokens[0]

    def suite(self, tokens):
        return добавить_отступ("\n" + "\n".join(tokens))

    def if_stmt(self, tokens):
        иначе_ = (f"\n{self.keys['else']}:" + tokens[3]) if tokens[3] else ""
        return "".join(
            [
                self.keys["if"],
                " ",
                tokens[0],
                ":",
                tokens[1],
                *(["\n", tokens[2]] if tokens[2] else ""),
                иначе_,
            ]
        )

    def elifs(self, tokens):
        return "\n".join(tokens)

    def elif_(self, tokens):
        return "".join([self.keys["elif"], " ", tokens[0], ":", tokens[1]])

    def import_from(self, tokens):
        return " ".join(
            [self.keys["from"], "".join(tokens[:-1]), self.keys["import"], tokens[-1]]
        )

    def import_name(self, tokens):
        return " ".join([self.keys["import"], tokens[0]])

    def dotted_as_name(self, tokens):
        return f" {self.keys['as']} ".join(пропустить_пустые(tokens))

    def import_as_name(self, tokens):
        return f" {self.keys['as']} ".join(пропустить_пустые(tokens))

    def dotted_as_names(self, tokens):
        return ", ".join(tokens)

    def import_as_names(self, tokens):
        return ", ".join(tokens)

    def dotted_name(self, tokens):
        return ".".join(tokens)

    def dots(self, tokens):
        return "".join(tokens)

    def global_stmt(self, tokens):
        return " ".join([self.keys["global"], ", ".join(tokens)])

    def nonlocal_stmt(self, tokens):
        return " ".join([self.keys["nonlocal"], ", ".join(tokens)])

    def assert_stmt(self, tokens):
        return " ".join([self.keys["assert"], ", ".join(пропустить_пустые(tokens))])

    def raise_stmt(self, tokens):
        return " ".join(
            [
                self.keys["raise"],
                f" {self.keys['from']} ".join(пропустить_пустые(tokens)),
            ]
        )

    def while_stmt(self, tokens):
        иначе_ = (f"\n{self.keys['else']}:" + tokens[2]) if tokens[2] else ""
        return "".join([self.keys["while"], " ", tokens[0], ":", tokens[1], иначе_])

    def continue_stmt(self, tokens):
        return self.keys["continue"]

    def break_stmt(self, tokens):
        return self.keys["break"]

    def assign(self, tokens):
        return " = ".join(tokens)

    def slice(self, tokens):
        tokens = [x or "" for x in tokens]
        return "{}:{}{}".format(*tokens)

    def sliceop(self, tokens):
        if tokens[0]:
            return f":{tokens[0]}"

    def var(self, tokens):
        return tokens[0]

    def test(self, tokens):
        return "{0} {3} {1} {4} {2}".format(*tokens, self.keys["if"], self.keys["else"])

    def star_expr(self, tokens):
        return f"*{tokens[0]}"

    def funccall(self, tokens):
        return f"{tokens[0]}({tokens[1] or ''})"

    def arguments(self, tokens):
        return ", ".join(пропустить_пустые(tokens))

    def argvalue(self, tokens):
        return "=".join(tokens)

    def starargs(self, tokens):
        return ", ".join(пропустить_пустые(tokens))

    def stararg(self, tokens):
        return f"*{tokens[0]}"

    def kwargs(self, tokens):
        return f"**{tokens[0]}"

    def subscript_tuple(self, tokens):
        return ", ".join(tokens)

    def parens(self, tokens):
        return f"({tokens[0]})"

    def getitem(self, tokens):
        return f"{tokens[0]}[{tokens[1]}]"

    def getattr(self, tokens):
        return ".".join(tokens)

    def NAME(self, token):
        return self.переводы.get(token, token)

    def annassign(self, tokens):
        if tokens[2]:
            return f"{tokens[0]}: {tokens[1]} = {tokens[2]}"
        return f"{tokens[0]}: {tokens[1]}"

    def augassign(self, tokens):
        return " ".join(tokens)

    def augassign_op(self, tokens):
        return tokens[0]

    def float(self, tokens):
        return tokens[0]

    def integer(self, tokens):
        return tokens[0]

    def complex(self, tokens):
        return tokens[0]

    def string(self, tokens):
        return tokens[0]

    def with_stmt(self, tokens):
        return "{2} {0}:{1}\n".format(*tokens, self.keys["with"])

    def with_items(self, tokens):
        return ", ".join(tokens)

    def with_item(self, tokens):
        return f" {self.keys['as']} ".join(пропустить_пустые(tokens))

    def STRING(self, token):
        if token[0] in "юбфрЮБФР":
            token = "ubfrUBFR"["юбфрЮБФР".index(token[0])] + token[1:]
        if token.lower().startswith("f"):
            result = []
            интерполяции = [0]
            скобка = False
            index = 0
            while index < len(token):
                if скобка:
                    скобка = False
                    index += 1
                    continue
                if token[index] == "{":
                    if token[index + 1 : index + 2] == "{":
                        скобка = True
                        continue
                    if not скобка:
                        интерполяции.append(index + 1)
                        index = проверка_интерполяции(token, index + 1)
                        интерполяции.append(index)
                скобка = False
                index += 1
            интерполяции.append(len(token))
            for index in range(len(интерполяции[:-1])):
                часть = token[интерполяции[index] : интерполяции[index + 1]]
                if index % 2:
                    часть_ = часть.split(":")
                    if len(часть_) > 1:
                        (
                            *часть,
                            фмт,
                        ) = часть_
                    else:
                        часть = часть_
                        фмт = None
                    часть = self.transform(
                        self.вычислительный_парсер.parse(":".join(часть))
                    )
                    result.append(":".join(пропустить_пустые([часть, фмт])))
                else:
                    result.append(часть)
            return "".join(result)
        return token

    def funcdef(self, tokens):
        return f"\n{self.keys['def']} {tokens[0]}({tokens[1] or ''}){' -> '.join(['', *пропустить_пустые([tokens[2]])])}: {tokens[3]}"

    def parameters(self, tokens):
        return ", ".join(пропустить_пустые(tokens))

    def paramvalue(self, tokens):
        return " = ".join(tokens)

    def const_true(self, tokens):
        return self.keys["True"]

    def const_false(self, tokens):
        return self.keys["False"]

    def const_none(self, tokens):
        return self.keys["None"]

    def starparams(self, tokens):
        return "".join(["*", ", ".join(пропустить_пустые(tokens))])

    def kwparams(self, tokens):
        return f"**{tokens[0]}"

    def typedparam(self, tokens):
        return ": ".join(tokens)

    def return_stmt(self, tokens):
        return " ".join([self.keys["return"], *пропустить_пустые(tokens)])

    def lambdef(self, tokens):
        return "".join(
            [self.keys["lambda"], с_пробелом(tokens[0] or ""), ": ", tokens[1]]
        )

    def lambda_params(self, tokens):
        return ", ".join(пропустить_пустые(tokens))

    def lambda_paramvalue(self, tokens):
        return "=".join(пропустить_пустые(tokens))

    def lambda_starparams(self, tokens):
        return ", ".join(пропустить_пустые(tokens))

    def lambda_kwparams(self, tokens):
        return f"**{tokens[0]}"

    def or_test(self, tokens):
        return f" {self.keys['or']} ".join(tokens)

    def and_test(self, tokens):
        return f" {self.keys['and']} ".join(tokens)

    def not_test(self, tokens):
        return f"{self.keys['not']} {tokens[0]}"

    def or_expr(self, tokens):
        return " | ".join(tokens)

    def xor_expr(self, tokens):
        return " ^ ".join(tokens)

    def and_expr(self, tokens):
        return " & ".join(tokens)

    def power(self, tokens):
        return " ** ".join(tokens)

    def comparison(self, tokens):
        return " ".join(tokens)

    def comp_op(self, tokens):
        return (
            tokens[0]
            .replace(self.keys["orig_not"], self.keys["not"])
            .replace(self.keys["orig_is"], self.keys["is"])
            .replace(self.keys["orig_in"], self.keys["in"])
        )

    def многострочный_список(self, tokens):
        return добавить_отступ("\n" + ",\n".join(tokens))

    def list(self, tokens):
        if len(tokens) > 5 or any("\n" in token for token in tokens):
            return "".join(["[", self.многострочный_список(tokens), "\n]"])
        return f"[{', '.join(tokens)}]"

    def dict(self, tokens):
        if len(tokens) > 5 or any("\n" in token for token in tokens):
            return "".join(["{", self.многострочный_список(tokens), "\n}"])
        return f"{{{', '.join(tokens)}}}"

    def set(self, tokens):
        if len(tokens) > 5 or any("\n" in token for token in tokens):
            return "".join(["{", self.многострочный_список(tokens), "\n}"])
        return f"{{{', '.join(tokens)}}}"

    def dict_comprehension(self, tokens):
        return f"{{{tokens[0]}}}"

    def shift_expr(self, tokens):
        return " ".join(tokens)

    def set_comprehension(self, tokens):
        return f"{{{tokens[0]}}}"

    def list_comprehension(self, tokens):
        return f"[{tokens[0]}]"

    def classdef(self, tokens):
        return "".join(
            [
                f"\n{self.keys['class']} ",
                tokens[0],
                f"({tokens[1]})" if tokens[1] else "",
                ":",
                tokens[2],
                "\n",
            ]
        )

    def comprehension(self, tokens):
        return " ".join(пропустить_пустые(tokens))

    def comp_fors(self, tokens):
        return " ".join(tokens)

    def comp_for(self, tokens):
        return " ".join(
            [
                *пропустить_пустые([f"{self.keys['async']} " if tokens[0] else ""]),
                self.keys["for"],
                tokens[1],
                self.keys["in"],
                tokens[2],
            ]
        )

    def comp_if(self, tokens):
        return f"{self.keys['if']} {tokens[0]}"

    def exprlist(self, tokens):
        return ", ".join(tokens)

    def yield_expr(self, tokens):
        return " ".join([self.keys["yield"], *пропустить_пустые(tokens)])

    def yield_from(self, tokens):
        return " ".join([self.keys["yield"], self.keys["from"], tokens[0]])

    def arith_expr(self, tokens):
        return " ".join(пропустить_пустые(tokens))

    def key_value(self, tokens):
        return ": ".join(tokens)

    def decorator(self, tokens):
        return "".join(["@", tokens[0], f"({tokens[1]})" if tokens[1] else ""])

    def decorators(self, tokens):
        return "\n".join(tokens)

    def decorated(self, tokens):
        return "".join(["\n", *tokens])

    def tuple(self, tokens):
        if tokens:
            if len(tokens) > 5 or all("\n" in token for token in tokens):
                return "".join(["(", self.многострочный_список(tokens), ",\n)"])
            return f"({', '.join(tokens)}, )"
        return "()"

    def testlist_tuple(self, tokens):
        return ", ".join(tokens)

    def simple_stmt(self, tokens):
        return "; ".join(tokens)

    def for_stmt(self, tokens):
        else_ = (f"\n{self.keys['else']}:" + tokens[3]) if tokens[3] else ""
        return "".join(
            [
                f"{self.keys['for']} ",
                tokens[0],
                f" {self.keys['in']} ",
                tokens[1],
                ":",
                tokens[2],
                else_,
            ]
        )

    def term(self, tokens):
        return " ".join(tokens)

    def factor(self, tokens):
        return " ".join(tokens)

    def async_funcdef(self, tokens):
        return " ".join([f"\n{self.keys['async']}", tokens[0][1:]])

    def del_stmt(self, tokens):
        return f"{self.keys['del']} {tokens[0]}"

    def await_expr(self, tokens):
        return f"{self.keys['await']} {tokens[0]}"

    def try_stmt(self, tokens):
        else_ = (f"{self.keys['else']}:" + tokens[2]) if tokens[2] else ""
        return "\n".join(
            пропустить_пустые(
                [
                    f"{self.keys['try']}: {tokens[0]}",
                    tokens[1],
                    else_ if tokens[2] else "",
                    tokens[3],
                    " ",
                ]
            )
        )

    def try_finally(self, tokens):
        return f"\n{self.keys['try']}: {tokens[0]}\n{tokens[1]}"

    def except_clauses(self, tokens):
        return "\n".join(tokens)

    def except_clause(self, tokens):
        if len(tokens) == 2:
            tokens.insert(1, None)
        return "".join(
            [
                self.keys["except"],
                с_пробелом(
                    f" {self.keys['as']} ".join(пропустить_пустые(tokens[:2]))
                ).rstrip(),
                ":",
                tokens[2],
            ]
        )

    def finally_(self, tokens):
        return f"{self.keys['finally']}: {tokens[0]}"

    def du_dct(self, tokens):
        return f"**{tokens[0]}"

    def pass_stmt(self, tokens):
        return self.keys["pass"]


def репорт(code, error, имя_файла="модуль"):
    номер_строки = error.line
    размер = 3
    верхний_размер = min(номер_строки - 1, размер)
    строки = code.split("\n")[номер_строки - верхний_размер - 1 : номер_строки + размер]
    отступ = error.column
    ширина_номера_строки = len(
        str(max(номер_строки - верхний_размер, номер_строки + размер))
    )
    return "\n".join(
        [
            *[
                f"{str(i + номер_строки - верхний_размер):>{ширина_номера_строки}} | {line}"
                for i, line in enumerate(строки[: верхний_размер + 1])
            ],
            f"{'':>{ширина_номера_строки + 1}}:{'':>{отступ}}^ Ошибка: Непредвиденный {error.token.type}",
            *[
                f"{str(i + 1 + номер_строки):>{ширина_номера_строки}} | {line}"
                for i, line in enumerate(строки[верхний_размер + 1 :])
            ],
        ]
    )


def transform(code, parser, преобразователь, имя_файла="модуль"):
    try:
        tree = parser.parse(code + "\n")
    except НепредвиденныйТокен as error:
        print(репорт(code, error, имя_файла))
        return None, None

    try:
        result = преобразователь.transform(tree)
    except Exception:
        print(format_exc())
        return None, tree

    return result, tree
