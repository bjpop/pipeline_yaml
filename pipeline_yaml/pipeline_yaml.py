'''
Module      : Main 
Description : The main entry point for the program.
Copyright   : (c) Bernie Pope, 2016 
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au
Portability : POSIX
'''

from __future__ import print_function
from argparse import ArgumentParser
import sys
import pkg_resources
import yaml
import graphviz as gv


PROGRAM_NAME = "pipeline_yaml"

try:
    PROGRAM_VERSION = pkg_resources.require(PROGRAM_NAME)[0].version
except pkg_resources.DistributionNotFound:
    PROGRAM_VERSION = "undefined_version"


def exit_with_error(message, exit_status):
    '''Print an error message to stderr, prefixed by the program name and 'ERROR'.
    Then exit program with supplied exit status.

    Arguments:
        message: an error message as a string.
        exit_status: a positive integer representing the exit status of the
            program.
    '''
    logging.error(message)
    print("{} ERROR: {}, exiting".format(PROGRAM_NAME, message), file=sys.stderr)
    sys.exit(exit_status)


def parse_args():
    '''Parse command line arguments.
    Returns Options object with command line argument values as attributes.
    Will exit the program on a command line error.
    '''
    parser = ArgumentParser(description='Render YAML pipeline as graph')
    parser.add_argument('--version',
        action='version',
        version='%(prog)s ' + PROGRAM_VERSION)
    parser.add_argument('yaml',
        metavar='FILE',
        type=str,
        help='Input YAML files')
    return parser.parse_args()


def process_data(graph, component):
    name = component['name']
    attribute = '\n'.join([attribute for attribute in component['attribute']])
    if attribute == "result":
        graph.node(name, shape = 'rectangle', style = 'filled', fillcolor='red')
    elif attribute == "reference":
        graph.node(name, shape = 'rectangle', style = 'filled', fillcolor='gold')
    elif attribute == "intermediate":
        graph.node(name, shape = 'rectangle', style = 'filled', fillcolor='grey')

#    graph.node(name, shape='rectangle')


def process_stage(graph, component):
    name = component['name']
    description = component['description']
    tool = '\n'.join([tool['name'] for tool in component['tools']])
#    caption = '{} {} {}'.format(tool,' ', name)
    graph.node(name, label = name+"\n"+ "(" + tool + ")")

def process_pipeline(graph, component):
    name = component['name']
    #graph.node(name)
    subgraph = gv.Digraph('cluster_' + name, graph_attr={'compound': 'true'})
    subgraph.body.append('label = "{}"'.format(name))
    subgraph.body.append('color=blue')
    components = component['components']
    dataflows = component['dataflows']
    process_components(subgraph, components)
    process_dataflows(subgraph, dataflows)
    graph.subgraph(subgraph)

def process_components(graph, components):
    for component in components:
        component_class = component['class']
        if component_class == 'data':
            process_data(graph, component)
        elif component_class == 'stage':
            process_stage(graph, component)
        elif component_class == 'pipeline':
            process_pipeline(graph, component)

def process_dataflows(graph, dataflows):
    for dataflow in dataflows:
        source = dataflow['source']
        destination = dataflow['destination']
        action =  dataflow['action']
        graph.edge(source, destination, label=action, fontsize='7')

def process_top_level(pipeline):
    if pipeline['class'] != 'pipeline':
        exit_with_error("Top level is not a pipeline definition", 1)
    name = pipeline['name']
    description = pipeline['description']
    components = pipeline['components']
    dataflows = pipeline['dataflows']
    toplevel_graph = gv.Digraph(name, format='png', graph_attr={'compound': 'true'}) 
    process_components(toplevel_graph, components)
    process_dataflows(toplevel_graph, dataflows)
    toplevel_graph.view()


def process_yaml(filename):
    with open(filename) as file:
        yaml_data = yaml.load(file)
        process_top_level(yaml_data)


def main():
    "Orchestrate the execution of the program"
    options = parse_args()
    print(options.yaml)
    process_yaml(options.yaml)


# If this script is run from the command line then call the main function.
if __name__ == '__main__':
    main()
