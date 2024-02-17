'''
This is a scrip that will be used in the setup.py as an entry point.
Instantiate all your classes here.
'''
import argparse
import sys
from main_project_package import project_root
from main_project_package.SimpleClass import SimpleClass


def parse_input_args(argv):
    ''' Parses command line arguments '''

    parser = argparse.ArgumentParser(description=
            "Description of the app that will be displayed when the script is executed.")
    parser.add_argument('--test', help="Test the app.", dest="test",
                        action='store_true', required=False)


def execute_script(input_args):
    config_file = "{}/config.yaml".format(project_root.path())
    parsed_args = parse_input_args(input_args)

    if parsed_args.test:
        print("Testing the app.")
        classObject = SimpleClass(config_file)


def main():
    # Entry point to the app. Call in test method
    execute_script(sys.argv[1:])


if __name__ == "__main__":
    main()