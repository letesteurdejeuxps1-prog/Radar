import pages.radar.Main as RadarMain
import pages.Variables as vars



def main():
    v = vars.Variables()
    rm = RadarMain.Main(v)
    rm.run()

if __name__ == '__main__':
    main()

