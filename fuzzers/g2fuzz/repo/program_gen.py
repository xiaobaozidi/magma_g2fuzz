import os
import sys
import argparse

def feature_analysis(model, file_format, tmp_path, seeds_path, generators, output_path, TRY_NUM):
    feature_programs = {} # key:feature    value:corresponding program
    print("++ 1. Get init features")
    messages_f = messages_for_feature(file_format)
    feature_pool, raw_output = reask_for_feature(messages_f, extract_res_for_feature, 3, model, 0.7) # feature_pool -> key:feature    value:feature descriptions
    messages_f.append({"role": "assistant", "content": raw_output})

    if not feature_pool:
        print(">> We failed to analyze the features for the given file format.")
        return 1
    print(">> init feature_head_pool:", feature_pool.keys())
    print("-- 1. Get init features")


    retry_cnt = 0
    try_cnt = 0
    generator_cnt = 1
    last_gen_cnt = count_files_in_directory(generators)
    print("++ 2. Analysis loop")
    while try_cnt < TRY_NUM:
        print("++++ 2.1 CUR EPOCH:", try_cnt)
        # print("\n========== EPOCH:", try_cnt, " ==========\n")
        # print("-- current feature_pool:", feature_pool)

        fail_cnt = 0
        all_cnt = 0
        print("++++++ 2.1.1 feature to generator")
        for feature in list(feature_pool.keys()):
            if feature in feature_programs.keys():
                print(">>>>>>>> 2.1.1.1 Has been analyzed:", feature)
                continue
            
            

            # feature_description = feature + feature_pool[feature]
            feature_description = feature_pool[feature]
            print("\n>>>>>>>> current feature:", feature_description)

            # generate a generator for each feature
            feature_try_cnt = 0
            while feature_try_cnt < 3:
                print(">>>>>>>> feature_try_cnt:", feature_try_cnt)
                print("++++++++ 2.1.1.1 generate init generator for feature:", feature)
                '''
                    - For the first epoch: Corresponding to the strategy 'Input Generator Synthesis'
                    - For the other epochs: Corresponding to the strategy 'Rare-Feature Directed Mutation' in 'Generator Mutation'
                '''
                if try_cnt == 0:
                    messages_c = messages_for_code_gen(file_format, feature_description)
                else:
                    # get a generator
                    generator_list = [f for f in os.listdir(generators) if os.path.isfile(os.path.join(generators, f))]
                    if len(generator_list) == 0:
                        messages_c = messages_for_code_gen(file_format, feature_description)
                    else:
                        target_generator = random.choice(generator_list)
                        target_generator_path = os.path.join(generators, target_generator)
                        print("Selected Generator:", target_generator_path)
                        with open(target_generator_path, 'r') as file:
                            target_generator_code = file.read()

                        messages_c = messages_for_generator_mutation(file_format, feature, feature_description, target_generator_code)
                generator = reask(messages_c, extract_res_for_code_gen, 3, 0.7, model)

                if not generator:
                    feature_try_cnt += 1
                    print(">>>>>>>> We can not generate corrresponding generator for this feature.")
                    continue
                
                print("-------- 2.1.1.1 generate init generator for feature:", feature_description)

                # print("---> generator:", generator)

                # execute the generator to get the target file
                # status, msg = validate_status_process(generator)
                # valid = status == ExecutionStatus.SUCCESS
                # print("---> status:", status, "msg:", msg)

                print("++++++++ 2.1.1.2 debug for generator")
                
                generated_code = self_debug(generator, 3, model, temperature = 0.2, output_path=os.path.dirname(tmp_path))
                if generated_code:
                    feature_programs[feature] = generated_code
                    mv_files(tmp_path, seeds_path, file_format + "-" + str(generator_cnt))

                    cur_generator_path = os.path.join(generators, file_format + "-" + str(generator_cnt) + ".py")
                    with open(cur_generator_path, 'w') as file:
                        file.write(generated_code) 
                    generator_cnt += 1

                    break                    
                
                feature_try_cnt += 1

                print("-------- 2.1.1.2 debug for generator")
            
            if feature_try_cnt == 3:
                fail_cnt += 1
                print(">>>>>>>> We can not generate the target code for this feature:", feature)
                del feature_pool[feature]

            
            all_cnt += 1

        print("------ 2.1.1 feature to generator")

        # if fail_cnt == all_cnt:
        #     print("All items can not generate executable programs -> finsh analysis")
        #     break
        
        if try_cnt >= TRY_NUM - 1:
            break

        print("++++++ 2.1.2 add more features")
        messages_f = messages_for_feature_reask(file_format, str(feature_pool.keys()))
        feature_pool_new, raw_output = reask_for_feature(messages_f, extract_res_for_feature, 3, model, 0.7)
        print("------ 2.1.2 add more features")

        print("++++++ 2.1.3 show added features")
        if not feature_pool_new:
            print(">>>>>> Can not continue analysis")
            break
        # print(">>>>>> feature_head_pool_new:", feature_pool_new.keys())

        repeat_cnt = 0
        for feature, description in feature_pool_new.items():
            if feature not in feature_pool.keys():
                feature_pool[feature] = description
            else:
                repeat_cnt += 1
                print("-", feature, "has existed")
        
        print(">>>>>> repeat_cnt:", repeat_cnt)
        print(">>>>>> new feature_head_pool:", feature_pool.keys())
        
        if repeat_cnt == len(feature_pool_new):
            print(">>>>>> All items are repeated -> finsh analysis")
            break
        
        print("------ 2.1.3 show added features")

        if count_files_in_directory(generators) > last_gen_cnt:
            retry_cnt = 0
            try_cnt += 1
            last_gen_cnt = count_files_in_directory(generators)
        else:
            retry_cnt += 1
            if retry_cnt > 3:
                break
            print("CURRENT EPOCH CAN NOT GET ANY NEW GENERATORS.")

        print("---- 2.2 CUR EPOCH:", try_cnt)

    for feature, description in feature_pool.items():
        print(">> ", feature, ":", description)
    
    print("-- 2. Analysis loop")

    with open(os.path.join(output_path, "feature_pool.json"), 'w') as file:
        json.dump(feature_pool, file)
    
    with open(os.path.join(output_path, "feature_programs.json"), 'w') as file:
        json.dump(feature_programs, file)





if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Description of your script.')
    parser.add_argument('--output', type=str, help='The path to store the output')
    parser.add_argument('--program', type=str, help='The target program')
    args = parser.parse_args()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(current_dir)
    from py_utils.func import *
    from py_utils.llm_analysis import *
    from py_utils.llm_utils import *

    with open('program_to_format.json', 'r') as file:
        program_to_format = json.load(file)

    with open('model_setting.json', 'r') as file:
        model_setting = json.load(file)

    if not os.path.exists(args.output):
        os.makedirs(args.output)
        os.makedirs(os.path.join(args.output, "default"))
    output_path = os.path.join(args.output, "default")

    model = model_setting["model"][0]
    print("model:", model)

    tmp_path = os.path.join(output_path, "tmp") # can not be changed
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)
    
    seeds_path = os.path.join(output_path, "gen_seeds")
    generators = os.path.join(output_path, "generators")
    if not os.path.exists(seeds_path):
        os.makedirs(seeds_path)
    if not os.path.exists(generators):
        os.makedirs(generators)

    start_time = time.time()
    file_formats = program_to_format[args.program]
    for file_format in file_formats:
        print("\n\n\n\n\n***************************")
        print("************", file_format , "************")
        print("***************************")
        try:
            '''
                If there are only one file format, we use both strategies: 'Input Generator Synthesis' and 'Rare-Feature Directed Mutation'.
                If there are multiple file formats, we only use the strategy 'Input Generator Synthesis' to migrate the overhead of seed generation.
                In `feature_analysis`, the first epoch is `Input Generator Synthesis`, and the other epochs are `Rare-Feature Directed Mutation`.
            '''
            if len(file_formats) == 1:
                feature_analysis(model, file_format, tmp_path, seeds_path, generators, output_path, 3) 
            else:
                feature_analysis(model, file_format, tmp_path, seeds_path, generators, output_path, 1) 
        except KeyboardInterrupt:
            print("You need install the following library to improve the fuzzing performance")
            for l in library_need_to_be_installed:
                print(l)

    if len(library_need_to_be_installed):
        print("You need install the following library to improve the fuzzing performance")
        for l in library_need_to_be_installed:
            print(l)

    # runtime
    end_time = time.time()
    run_time = end_time - start_time
    print("run_time: ", run_time)
    print("successful debug:", debug_cnt["successful"])
    print("failed debug:", debug_cnt["failed"])

    file_count = 0
    for _, _, files in os.walk(seeds_path):
        file_count += len(files)
    print("generated seeds num:", file_count)