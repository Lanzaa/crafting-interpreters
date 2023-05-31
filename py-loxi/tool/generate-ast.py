

import sys
from pathlib import Path


from typing import *

def defineAllAst(outputDir):
    defineAst(outputDir, "Expr", [
        "Binary : Expr left, Token operator, Expr right",
        "Grouping : Expr expression",
        "Literal : object value",
        "Unary : Token operator, Expr right",
        "Variable : Token name",
        "Assign : Token name, Expr value",
        ])
    defineAst(outputDir, "Stmt", [
        "Expression : Expr expression",
        "Print : Expr expression",
        "Var : Token name, Expr initializer",
        ])

def defineAst(outputDir, base_name: str, sub_types_lines: list):
    """
    each sub_type looks like:
    NameOfIt : Type nameOfValue1, Type nameOfValue2
    """

    p = Path(outputDir, base_name + ".py")

    if p.exists():
        raise Exception("Output file exists")

    with open(p, "w") as f:
        f.write("from dataclasses import dataclass\n\n")

        f.write(f"class {base_name}:\n  pass\n\n")

        parsed_types = []
        for line in sub_types_lines:
            sub_type = parseType(line)
            parsed_types.append(sub_type)

        for sub_type in parsed_types:
            f.write(typeToClass(base_name, sub_type))
            f.write("\n")
        f.write("\n")
        # Write a pattern match example

        f.write(f"def pattern_match_example(node: {base_name}):\n")
        f.write("  match node:\n")
        for name, sub_types in parsed_types:
            params = ", ".join( f"{pn}" for pn, t in sub_types.items())
            f.write(f"    case {name}({params}):\n")
            f.write(f"      pass\n")
        f.write(f"    case _:\n")
        f.write(f"      raise ValueError(\"Unknown type\")\n")
        f.write("\n")


        pass

def parseType(line: str) -> tuple:
    """
    > parseType("NameOfIt : Type nameOfValue1, Type nameOfValue2")
    ("NameOfIt", {"nameOfValue1": "Type", "nameOfValue2": "Type"})
    """
    name, params_defs = line.split(":")
    name = name.strip()
    params = {}
    for p in params_defs.strip().split(","):
        p_type, p_name = p.strip().split(" ")
        params[p_name] = p_type
    return (name, params)

def typeToClass(base, definition) -> str:
    """
    > typeToClass("X", ("NameOfIt", {"nameOfValue1": "Type", "nameOfValue2": "Type"}))
    @dataclass
    class NameOfIt(X):
      nameOfValue1: Type
      nameOfValue2: Type
    """
    name, params = definition
    out = ["@dataclass",
           f"class {name}({base}):"]
    for p_name, p_type in params.items():
        out.append(f"  {p_name}: {p_type}")
    out.append("")
    return "\n".join(out)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: generate-ast.py <output directory>")
        exit(64)
    defineAllAst(sys.argv[1])
