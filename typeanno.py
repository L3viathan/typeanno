import inspect
import ast


def make_restriction(ann, name):
    return eval(
        compile(
            ast.Expression(
                body=ast.Lambda(
                    args=ast.arguments(
                        args=[ast.arg(
                            arg=name,
                            lineno=1,
                            col_offset=0,
                        )],
                        posonlyargs=[],
                        kwonlyargs=[],
                        kw_defaults=[],
                        defaults=[],
                    ),
                    body=ann,
                    lineno=1,
                    col_offset=0,
                ),
            ),
            filename="<ast>",
            mode="eval",
        ),
    )


def restrict(cls):
    src = inspect.getsource(cls)
    mod = ast.parse(src)
    for statement in mod.body[0].body:
        if isinstance(statement, ast.AnnAssign):
            name = statement.target.id
            restriction = make_restriction(
                statement.annotation,
                name,
            )
        def getter(self):
            return getattr(self, f"_{name}")
        def setter(self, value):
            if restriction(value):
                setattr(self, f"_{name}", value)
            else:
                raise ValueError(
                    "Value {value!r} didn't pass check",
                )
        setattr(cls, name, property(fget=getter, fset=setter))
    return cls
