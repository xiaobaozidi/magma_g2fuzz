import os
import sys
import argparse

class TreeNode:
    def __init__(self, file_id, orig_name=None):
        self.file_id = file_id
        self.orig_name = orig_name
        self.children = []

def build_tree(file_names):
    file_map = {}  # Map file IDs to their respective TreeNode objects
    root_candidates = set()  # Store potential root candidates

    # First pass: create tree nodes for each file
    for file_name in file_names:
        parts = file_name.split(',')
        file_id = parts[0].split(':')[1]
        orig_name = None
        for part in parts[1:]:
            if 'orig:' in part:
                orig_name = part.split(':')[1].split('_')[0]  # Extract substring between "orig:" and "_"
                break
        if 'src:' not in file_name or '+' not in file_name.split('src:')[1]:
            root_candidates.add(file_id)  # Add files without two groups of numbers in src to root candidates
        file_map[file_id] = TreeNode(file_id, orig_name)

    # Second pass: build the tree structure
    for file_name in file_names:
        parts = file_name.split(',')
        file_id = parts[0].split(':')[1]
        src_id = None
        for part in parts[1:]:
            key_value = part.split(':')
            if len(key_value) == 2:
                key, value = key_value
                if key == 'src' and '+' not in value:
                    src_id = value
                    break
        if src_id:
            file_map[src_id].children.append(file_map[file_id])
            root_candidates.discard(file_id)  # Remove src files from root candidates

    # Find the root nodes
    roots = [file_map[root_id] for root_id in root_candidates]

    return roots

def print_tree(root, depth=0):
    if root is None:
        return 0
    # print('  ' * depth + '- ' + root.file_id)
    count = 1
    for child in root.children:
        count += print_tree(child, depth + 1)
    return count

def list_files(path):
    file_list = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    return file_list

generator_mutation_feature_prompt_init = '''
```
<TARGET_GENERATOR>
```

Based on the above code, provide me with a more complex code that can generate <FROMAT> files with additional more complex file features. 

Please respond according to the following template: 
Here's an extended version of the code that generates a <FROMAT> file with <more complex file features > such as <specific file features>: 
```
<Generated Code>
```
'''

generator_mutation_feature_prompt_incre = '''
Based on the above code, provide me with a more complex code that can generate <FROMAT> files with additional more complex file features. 

Please respond according to the following template: 
Here's an extended version of the code that generates a <FROMAT> file with <more complex file features > such as <specific file features>: 
```
<Generated Code>
```
'''

generator_mutation_structure_prompt_init = '''
```
<TARGET_GENERATOR>
```

Based on the above code, provide me with a more complex code that can generate <FROMAT> files with more complex file structures. 

Please respond according to the following template: 
Here's an extended version of the code that generates a <FROMAT> file with <more complex file structures > such as <specific file structures>: 
```
<Generated Code>
```
'''

generator_mutation_structure_prompt_incre = '''
Based on the above code, provide me with a more complex code that can generate <FROMAT> files with more complex file structures. 

Please respond according to the following template: 
Here's an extended version of the code that generates a <FROMAT> file with <more complex file structures > such as <specific file structures>: 
```
<Generated Code>
```
'''

pattern_based_mutation_prompt = '''
The original code:
```
<ORI>
```

The mutated code:
```
<MUT>
```

Imitate the mutation of 'The original code -> The mutated code' above and apply it to the following target code:
```
<TARGET_CODE>
```

Please respond according to the following template: 
"The mutated code" differs from "The original code" mainly in <changing/adding/... specific file features/structures>. We can apply the same mutation approach to the target code to obtain:
```
<The mutated code of the target code>
```
'''




def mutation_based_on_pattern(model, tmp_path, seeds_path, generators, output_path, mutation_log, relationship, mutation_pattern):
    cur_mutation_pattern = random.choice(mutation_pattern)
    ori_code_path = os.path.join(generators, cur_mutation_pattern[0]) 
    mutated_code_path = os.path.join(generators, cur_mutation_pattern[1]) 

    file_format = cur_mutation_pattern[0].split('-')[0]

    with open(ori_code_path, 'r') as file:
        ori_code = file.read()
    
    with open(mutated_code_path, 'r') as file:
        mutated_code = file.read()


    # get a generator
    generator_list = [f for f in os.listdir(generators) if os.path.isfile(os.path.join(generators, f))]
    # target_generator = random.choice(generator_list)
    filtered_list = [s for s in generator_list if s.startswith(file_format)]
    target_generator = random.choice(filtered_list)
    # target_generator = 'tiff-2.py'
    target_generator_path = os.path.join(generators, target_generator)
    print(target_generator_path)
    with open(target_generator_path, 'r') as file:
        target_generator_code = file.read()
    
    target_generator_log = [
        {"role": "system", "content": "You are an advanced Language Model assistant that can generate, execute, and evaluate code. Please use Markdown syntax to represent code blocks."},
    ]
    prompt = copy.deepcopy(pattern_based_mutation_prompt)
    prompt = prompt.replace("<ORI>", ori_code)
    prompt = prompt.replace("<MUT>", mutated_code)
    prompt = prompt.replace("<TARGET_CODE>", target_generator_code)
    target_generator_log.append({"role": "user", "content": prompt})


    # get raw llm
    mutated_generator, raw_llm = gen_code_debug(target_generator_log, 3, model, 0.7)

    # debug the code
    mutated_generator_debuged = self_debug(mutated_generator, 6, model, temperature = 0.2, output_path=os.path.dirname(tmp_path))
    if mutated_generator_debuged:
        generator_cnt = count_files_in_directory(generators) + 1

        mv_files(tmp_path, seeds_path, file_format + "-" + str(generator_cnt))

        cur_generator_path = os.path.join(generators, file_format + "-" + str(generator_cnt) + ".py")
        with open(cur_generator_path, 'w') as file:
            file.write(mutated_generator_debuged) 

        return True
    else:
        return False


def mutation_based_on_predefined_mutators(model, tmp_path, seeds_path, generators, output_path, mutation_log, cur_mutator):

    if cur_mutator == "feature": # file feature mutation
        prompt_init = copy.deepcopy(generator_mutation_feature_prompt_init)
        prompt_incre = copy.deepcopy(generator_mutation_feature_prompt_incre)
    else: # file structure mutation
        prompt_init = copy.deepcopy(generator_mutation_structure_prompt_init)
        prompt_incre = copy.deepcopy(generator_mutation_structure_prompt_incre)

    # read the relationship
    relationship_path = os.path.join(mutation_log, "relationship.json")
    if os.path.exists(relationship_path):
        with open(relationship_path, 'r') as file:
            relationship = json.load(file)
    else:
        relationship = {}

    # step I: get a generator
    generator_list = [f for f in os.listdir(generators) if os.path.isfile(os.path.join(generators, f))]
    target_generator = random.choice(generator_list)
    # target_generator = 'tiff-2.py'
    file_format = target_generator.split('-')[0]
    target_generator_path = os.path.join(generators, target_generator)
    print(target_generator_path)
    with open(target_generator_path, 'r') as file:
        target_generator_code = file.read()
    
    target_generator_log = [
        {"role": "system", "content": "You are an advanced Language Model assistant that can generate, execute, and evaluate code. Please use Markdown syntax to represent code blocks."},
    ]
    init = copy.deepcopy(prompt_init)
    init = init.replace("<FROMAT>", file_format)
    init = init.replace("<TARGET_GENERATOR>", target_generator_code)
    target_generator_log.append({"role": "user", "content": init})
    # print(target_generator_log[-1]["content"])
    

    # get raw llm
    mutated_generator, raw_llm = gen_code_debug(target_generator_log, 3, model, 0.7)

    # debug the code
    mutated_generator_debuged = self_debug(mutated_generator, 6, model, temperature = 0.2, output_path=os.path.dirname(tmp_path))
    if mutated_generator_debuged:
        # if debug successfully, replace the wrong code with the right code
        raw_llm.replace(mutated_generator, mutated_generator_debuged)

        generator_cnt = count_files_in_directory(generators) + 1

        mv_files(tmp_path, seeds_path, file_format + "-" + str(generator_cnt))

        cur_generator_path = os.path.join(generators, file_format + "-" + str(generator_cnt) + ".py")
        with open(cur_generator_path, 'w') as file:
            file.write(mutated_generator_debuged) 

        # # get seeds
        # mv_files(tmp_path, seeds_path, os.path.splitext(target_generator)[0])

        # save the relationship
        if target_generator not in relationship.keys():
            relationship[target_generator] = [file_format + "-" + str(generator_cnt) + ".py"]
        else:
            relationship[target_generator].append(file_format + "-" + str(generator_cnt) + ".py")
        with open(relationship_path, 'w') as file:
            json.dump(relationship, file)
        
        return True
    else:
        return False

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Description of your script.')
    parser.add_argument('--output', type=str, help='The path to store the output')
    args = parser.parse_args()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(current_dir)
    from py_utils.func import *
    from py_utils.llm_analysis import *
    from py_utils.llm_utils import *

    output_path = args.output

    with open('model_setting.json', 'r') as file:
        model_setting = json.load(file)

    model = model_setting["model"][0]
    print("model:", model)

    tmp_path = os.path.join(args.output, "tmp") # can not be changed
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)

    seeds_path = os.path.join(args.output, "gen_seeds")
    generators = os.path.join(args.output, "generators")
    mutation_log = os.path.join(args.output, "mutation_log")
    if not os.path.exists(seeds_path):
        os.makedirs(seeds_path)
    if not os.path.exists(generators):
        os.makedirs(generators)
    if not os.path.exists(mutation_log):
        os.makedirs(mutation_log)

    mutators = ["feature", "structure"]

    # read the relationship
    relationship_path = os.path.join(mutation_log, "relationship.json")
    if os.path.exists(relationship_path):
        with open(relationship_path, 'r') as file:
            relationship = json.load(file)
    else:
        relationship = None
    
    if relationship:
        # get successfully mutation
        mutation_pattern = []
        file_names = list_files(os.path.join(output_path, "queue"))
        roots = build_tree(file_names)
        for root in roots:
            num_nodes = print_tree(root)
            if num_nodes - 1 > 0:
                cur = root.orig_name + ".py"
                print("ID:", root.file_id)
                print("Original generator:", cur)
                print("Number of sub-nodes:", num_nodes - 1)  # Subtract 1 for the root node
                print("\n")

                for ori, mutated in relationship.items():
                    if cur in mutated:
                        mutation_pattern.append([ori, cur])

        print("mutation_pattern:", mutation_pattern)

        if len(mutation_pattern) != 0:
            mutators.append("pattern")

    print("mutators:", mutators)
    cur_mutator = random.choice(mutators)
    print("cur_mutator:", cur_mutator)

    if cur_mutator == "pattern":
        mutation_based_on_pattern(model, tmp_path, seeds_path, generators, output_path, mutation_log, relationship, mutation_pattern)
    else:
        mutation_based_on_predefined_mutators(model, tmp_path, seeds_path, generators, output_path, mutation_log, cur_mutator)