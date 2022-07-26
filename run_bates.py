import argparse

from bates import bates


def main():
    parser = argparse.ArgumentParser(
        description='Change string prefix of Bates number')
    parser.add_argument('dirname', type=str,
                        help='directory with the unstamped files')
    parser.add_argument('--prefix', type=str,
                        help='string prefix for the Bates number', default='')
    parser.add_argument('--x', help='horizontal position of text', type=int,
                        default=300)
    parser.add_argument('--y', help='vertical position of text', type=int,
                        default=30)
    parser.add_argument('--rotation', help='rotation of the text', type=int,
                        default=0)
    parser.add_argument('--no-manual',
                        help='whether to manually set the text position.'
                        'True if called, false otherwise',
                        action='store_true')
    args = parser.parse_args()
    if args.no_manual:
        manual = False
    else:
        manual = True
    bates(dirname=args.dirname, prefix=args.prefix, x=args.x, y=args.y,
          rotation=args.rotation, manual=manual)


main()
