

import sys
from pathlib import Path


from typing import *

def defineAllAst(outputDir):
    defineAst(outputDir, "Expr", [
        "Binary : Expr left, Token operator, Expr right",
        "Grouping : Expr expression",
        "Literal : Object value",
        "Unary : Token operator, Expr right",
        ])

def defineAst(outputDir, base_name: str, sub_types: list):
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

        for sub_type in sub_types:
            f.write(typeToClass(base_name, sub_type))
            f.write("\n")

def typeToClass(base, line: str) -> str:
    """
    > typeToClass("X", "NameOfIt : Type nameOfValue1, Type nameOfValue2")
    @dataclass
    class NameOfIt(X):
      nameOfValue1: Type
      nameOfValue2: Type
    """
    name, params = line.split(":")
    out = [
      "@dataclass",
      f"class {name}({base}):"
    ]
    for p in params.strip().split(","):
        p_type, p_name = p.strip().split(" ")
        out.append(f"  {p_name}: {p_type}")
    out.append("")
    return "\n".join(out)





if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: generate-ast.py <output directory>")
        exit(64)
    defineAllAst(sys.argv[1])
