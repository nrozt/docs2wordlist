#! /usr/bin/env python3

import argparse
import os
import json
import random
import urllib.parse


def write_set_to_output_file(data, filename):
    data = list(data)
    data.sort()
    out_buffer = '\n'.join(data)
    if filename:
        if filename == '-':
            print(out_buffer)
        else:
            with open(filename, 'w') as f:
                f.write(out_buffer + '\n')


def generate_parameter_value(name, param_type, enum=None):
    if enum:
        return random.choice(enum)
    if param_type == 'string':
        return f'str_arg_{name}'
    mock_values = {
        'array': '[array_param]',
        'boolen': 'true',
        'int': 1,
        'integer': 1,
        'number': 1
    }
    return mock_values.get(param_type)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="DESC"
    )
    parser.add_argument("-i", "--input", help="Path to input file", required=True)
    parser.add_argument('-o', '--output', help='Path to URLs output file. Use "-" to print to stdin', required=False)
    parser.add_argument('-m', '--methods', help='Add methods to URLs', action='store_true', required=False)
    parser.add_argument('-q', '--query-params', help='Add query parameters to URLs', action='store_true', required=False)
    parser.add_argument('-op', '--output-params', help='Path to parameters output file. Use "-" to print to stdin', required=False)
    parser.add_argument('-ope', help='Add example values to parameters output file', action='store_true', required=False)
    parser.add_argument('-oh', '--output-headers', help='Path to headers output file. Use "-" to print to stdin', required=False)
    parser.add_argument('-ohe', help='Add example values to headers output file', action='store_true', required=False)

    args = parser.parse_args()
    if not (args.output or args.output_params or args.output_headers):
        args.output = '-'

    all_urls = set()
    all_parameters = set()
    all_headers = set()

    with open(args.input, 'r') as f:
        swagger = json.load(f)

    for path, methods in swagger.get('paths', dict()).items():
        common_params = list()
        for method in methods.keys():
            if method == 'parameters':
                common_params += methods[method]

            else:
                real_path = path
                if real_path.startswith('/'):
                    real_path = real_path[1:]
                query_params = dict()
                headers = dict()
                for parameter in methods[method].get('parameters', list()) + common_params:
                    param_type = parameter.get('type', parameter.get('schema', {}).get('type'))
                    if parameter.get('in') == 'path':
                        value = generate_parameter_value(
                            parameter.get('name'),
                            param_type,
                            parameter.get('enum')
                        )
                        if value:
                            real_path = real_path.replace('{' + parameter.get('name') + '}', str(value))

                    elif parameter.get('in') == 'query':
                        query_params[parameter.get('name')] = generate_parameter_value(
                            parameter.get('name'),
                            param_type,
                            parameter.get('enum')
                        )
                    elif parameter.get('in') == 'header':
                        headers[parameter.get('name')] = generate_parameter_value(
                            parameter.get('name'),
                            param_type,
                            parameter.get('enum')
                        )
                if query_params and args.query_params:
                    str_query_params = f'?{urllib.parse.urlencode(query_params)}'
                else:
                    str_query_params = ''
                
                if args.output:
                    if args.methods:
                        all_urls.add(f'{method.upper()} {real_path}{str_query_params}')
                    else:
                        all_urls.add(f'{real_path}{str_query_params}')

                if args.output_params:
                    for parameter, value in query_params.items():
                        if args.ope:
                            all_parameters.add(f'{parameter}={value}')
                        else:
                            all_parameters.add(parameter)

                if args.output_headers:
                    for header, value in headers.items():
                        if args.ohe:
                            all_headers.add(f'{header}: {value}')
                        else:
                            all_headers.add(header)
                


    write_set_to_output_file(all_urls, args.output)
    write_set_to_output_file(all_parameters, args.output_params)
    write_set_to_output_file(all_headers, args.output_headers)

