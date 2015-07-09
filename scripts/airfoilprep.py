#!/usr/bin/env python

from airfoilprep import *

if __name__ == '__main__':

    import os
    from argparse import ArgumentParser, RawTextHelpFormatter

    # setup command line arguments
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter,
                            description='Preprocessing airfoil data for wind turbine applications.')
    parser.add_argument('src_file', type=str, help='source file')
    parser.add_argument('--stall3D', type=str, nargs=3, metavar=('r/R', 'c/r', 'tsr'), help='2D data -> apply 3D corrections')
    parser.add_argument('--extrap', type=str, nargs=1, metavar=('cdmax'), help='3D data -> high alpha extrapolations')
    parser.add_argument('--blend', type=str, nargs=2, metavar=('otherfile', 'weight'), help='blend 2 files weight 0: sourcefile, weight 1: otherfile')
    parser.add_argument('--out', type=str, help='output file')
    parser.add_argument('--plot', action='store_true', help='plot data using matplotlib')
    parser.add_argument('--common', action='store_true', help='interpolate the data at different Reynolds numbers to a common set of angles of attack')


    # parse command line arguments
    args = parser.parse_args()
    fileOut = args.out

    if args.plot:
        import matplotlib.pyplot as plt

    # perform actions
    if args.stall3D is not None:

        if fileOut is None:
            name, ext = os.path.splitext(args.src_file)
            fileOut = name + '_3D' + ext

        af = Airfoil.initFromAerodynFile(args.src_file)
        floats = [float(var) for var in args.stall3D]
        af3D = af.correction3D(*floats)

        if args.common:
            af3D = af3D.interpToCommonAlpha()

        af3D.writeToAerodynFile(fileOut)

        if args.plot:

            for p, p3D in zip(af.polars, af3D.polars):
                # plt.figure(figsize=(6.0, 2.6))
                # plt.subplot(121)
                plt.figure()
                plt.plot(p.alpha, p.cl, 'k', label='2D')
                plt.plot(p3D.alpha, p3D.cl, 'r', label='3D')
                plt.xlabel('angle of attack (deg)')
                plt.ylabel('lift coefficient')
                plt.legend(loc='lower right')

                # plt.subplot(122)
                plt.figure()
                plt.plot(p.alpha, p.cd, 'k', label='2D')
                plt.plot(p3D.alpha, p3D.cd, 'r', label='3D')
                plt.xlabel('angle of attack (deg)')
                plt.ylabel('drag coefficient')
                plt.legend(loc='upper center')

                # plt.tight_layout()
                # plt.savefig('/Users/sning/Dropbox/NREL/SysEng/airfoilpreppy/docs/images/stall3d.pdf')

            plt.show()


    elif args.extrap is not None:

        if fileOut is None:
            name, ext = os.path.splitext(args.src_file)
            fileOut = name + '_extrap' + ext

        af = Airfoil.initFromAerodynFile(args.src_file)

        afext = af.extrapolate(float(args.extrap[0]))

        if args.common:
            afext = afext.interpToCommonAlpha()

        afext.writeToAerodynFile(fileOut)

        if args.plot:

            for p, pext in zip(af.polars, afext.polars):
                # plt.figure(figsize=(6.0, 2.6))
                # plt.subplot(121)
                plt.figure()
                p1, = plt.plot(pext.alpha, pext.cl, 'r')
                p2, = plt.plot(p.alpha, p.cl, 'k')
                plt.xlabel('angle of attack (deg)')
                plt.ylabel('lift coefficient')
                plt.legend([p2, p1], ['orig', 'extrap'], loc='upper right')

                # plt.subplot(122)
                plt.figure()
                p1, = plt.plot(pext.alpha, pext.cd, 'r')
                p2, = plt.plot(p.alpha, p.cd, 'k')
                plt.xlabel('angle of attack (deg)')
                plt.ylabel('drag coefficient')
                plt.legend([p2, p1], ['orig', 'extrap'], loc='lower right')

                plt.figure()
                p1, = plt.plot(pext.alpha, pext.cm, 'r')
                p2, = plt.plot(p.alpha, p.cm, 'k')
                plt.xlabel('angle of attack (deg)')
                plt.ylabel('moment coefficient')
                plt.legend([p2, p1], ['orig', 'extrap'], loc='upper right')

                # plt.tight_layout()
                # plt.savefig('/Users/sning/Dropbox/NREL/SysEng/airfoilpreppy/docs/images/extrap.pdf')

            plt.show()


    elif args.blend is not None:

        if fileOut is None:
            name1, ext = os.path.splitext(args.src_file)
            name2, ext = os.path.splitext(os.path.basename(args.blend[0]))
            fileOut = name1 + '+' + name2 + '_blend' + args.blend[1] + ext

        af1 = Airfoil.initFromAerodynFile(args.src_file)
        af2 = Airfoil.initFromAerodynFile(args.blend[0])
        afOut = af1.blend(af2, float(args.blend[1]))

        if args.common:
            afOut = afOut.interpToCommonAlpha()

        afOut.writeToAerodynFile(fileOut)



        if args.plot:

            for p in afOut.polars:
                fig = plt.figure()
                ax = fig.add_subplot(111)
                plt.plot(p.alpha, p.cl, 'k')
                plt.xlabel('angle of attack (deg)')
                plt.ylabel('lift coefficient')
                plt.text(0.6, 0.2, 'Re = ' + str(p.Re/1e6) + ' million', transform=ax.transAxes)

                fig = plt.figure()
                ax = fig.add_subplot(111)
                plt.plot(p.alpha, p.cd, 'k')
                plt.xlabel('angle of attack (deg)')
                plt.ylabel('drag coefficient')
                plt.text(0.2, 0.8, 'Re = ' + str(p.Re/1e6) + ' million', transform=ax.transAxes)

                fig = plt.figure()
                ax = fig.add_subplot(111)
                plt.plot(p.alpha, p.cm, 'k')
                plt.xlabel('angle of attack (deg)')
                plt.ylabel('moment coefficient')
                plt.text(0.2, 0.8, 'Re = ' + str(p.Re/1e6) + ' million', transform=ax.transAxes)

            plt.show()
