import sys
from .interface import Session

DEFAULT_WIDTH = 20
DEFAULT_HEIGHT = 12
DEFAULT_DENSITY = .6

def main():
    if "--help" in sys.argv:
        print("")
        print(f"   -w <N>   Set width to N spaces. Default = {DEFAULT_WIDTH}")
        print(f"   -h <N>   Set height to N spaces. Default = {DEFAULT_HEIGHT}")
        print(f"   -d <N>   Set density to N  (0-1). Default = {DEFAULT_DENSITY}")
        print("------------Controls------------")
        print(f"    {Session.CTL_UP},{Session.CTL_DOWN},{Session.CTL_LEFT},{Session.CTL_RIGHT}  Move Cursor")
        print(f"    {Session.CTL_SET}        Fill Cell")
        print(f"    {Session.CTL_BLOCK}        Block Cell")
        print(f"    {Session.CTL_UNDO}        Undo")
        print(f"    {Session.CTL_QUIT}        Quit")
        print("")
        sys.exit()

    try:
        w_index = sys.argv.index('-w')
        width = sys.argv[w_index + 1]
    except ValueError:
        width = DEFAULT_WIDTH

    try:
        h_index = sys.argv.index('-h')
        height = sys.argv[h_index + 1]
    except ValueError:
        height = DEFAULT_HEIGHT

    try:
        d_index = sys.argv.index('-d')
        density = sys.argv[d_index + 1]
    except ValueError:
        density = DEFAULT_DENSITY

    try:
        if int(width) <= 0:
            raise ValueError()
    except ValueError:
        print("-w requires valid integer > 0")
        sys.exit()

    try:
        if int(height) <= 0:
            raise ValueError()
    except ValueError:
        print("-h requires valid integer > 0")
        sys.exit()

    try:
        if float(density) <= 0 or float(density) > 1:
            raise ValueError()
    except ValueError:
        print("-d requires valid float between 0 & 1")
        sys.exit()

    session = Session(width=int(width), height=int(height), density=float(density))
    session.play()

if __name__ == "__main__":
    main()