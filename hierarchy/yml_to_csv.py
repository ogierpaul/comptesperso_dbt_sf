import os
from tree2tabular import TreeBuilder

def read_file(fn:str) -> TreeBuilder:
    tree = TreeBuilder.from_yaml(fn)
    return tree

def output_seed(tree:TreeBuilder, output_fn:str):
    tree.to_csv(output_fn, overwrite=True)

def create_category_hierarchy_main():
    projdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_fn = os.path.join(projdir, 'hierarchy', 'categorytree_with_ids.yml')
    output_fn = os.path.join(projdir, 'comptesperso_dbt_sf', 'seeds', 'categorytree.csv')
    tree = read_file(input_fn)
    output_seed(tree, output_fn)
    pass


if __name__ == '__main__':
    create_category_hierarchy_main()