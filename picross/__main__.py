import sys
from interface import Session

DEFAULT_WIDTH = 20
DEFAULT_HEIGHT = 12
DEFAULT_DENSITY = .6

if __name__ == "__main__":
    try:
        help_index = sys.argv.index("--help")
        print(f"   -w <N>   Set width to N spaces. Default = {DEFAULT_WIDTH}")
        print(f"   -h <N>   Set height to N spaces. Default = {DEFAULT_HEIGHT}")
        print(f"   -d <N>   Set density to N  (0-1). Default = {DEFAULT_DENSITY}")
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
        WIDTH = sys.argv[w_index + 1]
    except ValueError:
        WIDTH = DEFAULT_WIDTH

    try:
        h_index = sys.argv.index('-h')
        HEIGHT = sys.argv[h_index + 1]
    except ValueError:
        HEIGHT = DEFAULT_HEIGHT

    try:
        d_index = sys.argv.index('-d')
        DENSITY = sys.argv[d_index + 1]
    except ValueError:
        DENSITY = DEFAULT_DENSITY

    try:
        if int(WIDTH) <= 0:
            raise ValueError()
    except ValueError:
        print("-w requires valid integer > 0")
        sys.exit()

    try:
        if int(HEIGHT) <= 0:
            raise ValueError()
    except ValueError:
        print("-h requires valid integer > 0")
        sys.exit()

    try:
        if float(DENSITY) <= 0 or float(DENSITY) > 1:
            raise ValueError()
    except ValueError:
        print("-d requires valid float between 0 & 1")
        sys.exit()

    session = Session(width=int(WIDTH), height=int(HEIGHT), density=float(DENSITY))
    session.play()
