import os
import pages.radar.Main as RadarMain
import pages.Variables as Vars


def main():
    v = Vars.Variables()
    rm = RadarMain.Main(v, os.getcwd())
    rm.run()


if __name__ == '__main__':
    main()
