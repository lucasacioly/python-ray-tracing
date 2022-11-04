import argparse

class Parser:

    def __init__(self):
        parser = argparse.ArgumentParser(description = 'img input/output')

        parser.add_argument( 
            type=str, 
            required = True, 
            metavar='', 
            help ='input path'
        )

        parser.add_argument(
            type=str, 
            required = True, 
            metavar='', 
            help ='output path'
        )

    
