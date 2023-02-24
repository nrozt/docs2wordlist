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


def get_items_requests(items):
    requests = list()
    for item in items:
        if 'request' in item.keys():
            requests.append(item['request'])
        if 'item' in item.keys():
            requests += get_items_requests(item['item'])
    return requests


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
        postman = json.load(f)

    if 'item' in postman.keys():
        requests = get_items_requests(postman['item'])
    else:
        requests = list()

    urls = set()
    all_headers = set()
    all_parameters = set()
    for request in requests:
        url = '/'.join([i for i in request['url']['path'] if i])
        parameters = {p.get('key'): p.get('value') for p in request['url'].get('query', list())}
        headers = {h.get('key'): h.get('value') for h in request.get('header', list())}
        if 'auth' in request.keys() and request['auth']['type'] != 'noauth':
            auth_type = request['auth']['type']
            headers['Authorization'] = '{} {}'.format(auth_type, request['auth'][auth_type][0]['value'])

        method = request['method']
        if parameters and args.query_params:
            str_query_params = f'?{urllib.parse.urlencode(parameters)}'
        else:
            str_query_params = ''

        if args.output:
            if args.methods:
                urls.add(f'{method.upper()} {url}{str_query_params}')
            else:
                urls.add(f'{url}{str_query_params}')

        if args.output_params:
            for parameter, value in parameters.items():
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

    write_set_to_output_file(urls, args.output)
    write_set_to_output_file(all_parameters, args.output_params)
    write_set_to_output_file(all_headers, args.output_headers)
