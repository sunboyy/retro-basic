#! /usr/bin/env python3
from argparse import ArgumentParser
from compiler.scanner import tokenize
from compiler.parser import parse
from compiler.code_generator import generate

if __name__ == "__main__":
    argParser = ArgumentParser(description='Compile Retro Basic language into bytecode')
    argParser.add_argument('source', help='Source path')
    argParser.add_argument('-o', '--output', help='Output path')
    args = argParser.parse_args()

    infile = open(args.source)
    data = infile.read()
    infile.close()

    tokens = tokenize(data)
    parse_tree = parse(tokens)
    # print(parse_tree)
    bytecode = ' '.join([str(e) for e in generate(parse_tree)])
    if args.output is not None:
        with open(args.output, 'w') as outfile:
            outfile.write(bytecode)
    else:
        print(bytecode)
