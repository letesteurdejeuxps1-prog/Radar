import os
import pages.radar.Main as RadarMain
import pages.Variables as Vars


def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    v = Vars.Variables()
    rm = RadarMain.Main(v, os.getcwd())
    rm.run()


if __name__ == '__main__':
    main()
