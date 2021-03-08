from __future__ import annotations

from typeanno import restrict

@restrict
class Test:
    x: 0 < x < 10
    def __init__(self, x):
        self.x = x

if __name__ == '__main__':
    t = Test(7)
    print(t.x, "is 7")
    t.x = 3
    print(t.x, "is 3")
    try:
        t.x = 12
        print("This won't be printed")
    except ValueError:
        print("Couldn't set property")
