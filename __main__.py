import sys
from interface import Session

default_width = 20
default_height = 12
default_density = .6
try:
    help_index = sys.argv.index("--help")
    print(f"   -w <N>   Set width to N spaces. Default = {default_width}")
    print(f"   -h <N>   Set height to N spaces. Default = {default_height}")
    print(f"   -d <N>   Set density to N  (0-1). Default = {default_density}")
    print("------------Controls------------")
    print(f"    {Session.CTL_UP},{Session.CTL_DOWN},{Session.CTL_LEFT},{Session.CTL_RIGHT}  Move Cursor")
    print(f"    {Session.CTL_SET}        Fill Cell")
    print(f"    {Session.CTL_BLOCK}        Block Cell")
    print(f"    {Session.CTL_UNDO}        Undo")
    print(f"    {Session.CTL_QUIT}        Quit")
    sys.exit()
except ValueError:
    pass

try:
    w_index = sys.argv.index('-w')
    w = sys.argv[w_index + 1]
except ValueError:
    w = default_width

try:
    h_index = sys.argv.index('-h')
    h = sys.argv[h_index + 1]
except ValueError:
    h = default_height

try:
    d_index = sys.argv.index('-d')
    d = sys.argv[d_index + 1]
except ValueError:
    d = default_density

try:
    if int(w) <= 0:
        raise ValueError()
except ValueError:
    print("-w requires valid integer > 0")
    sys.exit()

try:
    if int(h) <= 0:
        raise ValueError()
except ValueError:
    print("-h requires valid integer > 0")
    sys.exit()

try:
    if float(d) <= 0 or float(d) > 1:
        raise ValueError()
except ValueError:
    print("-d requires valid float between 0 & 1")
    sys.exit()


session = Session(width=int(w), height=int(h), density=float(d))
session.play()
