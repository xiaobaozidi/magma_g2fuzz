import argparse
import openai
import copy
import re
import os
import shutil
import time
import subprocess
from collections import Counter
from enum import IntEnum, auto
import json 
import random
from .llm_utils import *

CURRENT_TIME = time.time()

class ExecutionStatus(IntEnum):
    SUCCESS = auto()
    EXCEPTION = auto()
    CRASH = auto()
    NOTCALL = auto()
    TIMEOUT = auto()

def run_cmd(
    cmd_args,
    timeout=10,
    verbose=False,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    shell=False,
    cwd=None,
) -> (ExecutionStatus, str):
    try:
        output = subprocess.run(
            cmd_args, stdout=stdout, stderr=stderr, timeout=timeout, shell=shell, cwd=cwd
        )
    except subprocess.TimeoutExpired as te:
        if verbose:
            print("Timed out")
        return ExecutionStatus.TIMEOUT, ""
    else:
        if verbose:
            print("output.returncode: ", output.returncode)
        if output.returncode != 0:
            # 134 = Crash
            # 1 = exception
            error_msg = ""
            if output.stdout is not None:
                stdout_msg = output.stdout.decode("utf-8")
                stderr_msg = output.stderr.decode("utf-8")
                if verbose:
                    print("stdout> ", stdout_msg)
                if verbose:
                    print("stderr> ", stderr_msg)
                stdout_msg = stdout_msg[:30]
                error_msg = "---- returncode={} ----\nstdout> {}\nstderr> {}\n".format(
                    output.returncode, stdout_msg, stderr_msg
                )

            if output.returncode == 134:  # Failed assertion
                return ExecutionStatus.CRASH, "SIGABRT Triggered\n" + error_msg
            elif output.returncode == 132:
                return ExecutionStatus.CRASH, "SIGILL\n" + error_msg
            elif output.returncode == 133:
                return ExecutionStatus.CRASH, "SIGTRAP\n" + error_msg
            elif output.returncode == 136:
                return ExecutionStatus.CRASH, "SIGFPE\n" + error_msg
            elif output.returncode == 137:
                return ExecutionStatus.CRASH, "OOM\n" + error_msg
            elif output.returncode == 138:
                return ExecutionStatus.CRASH, "SIGBUS Triggered\n" + error_msg
            elif output.returncode == 139:
                return (
                    ExecutionStatus.CRASH,
                    "Segmentation Fault Triggered\n" + error_msg,
                )
            else:
                if output.returncode != 1:
                    # Check Failed: -6
                    print("output.returncode: ", output.returncode)
                    print(cmd_args)
                    print("stdout> ", stdout_msg)
                    print("stderr> ", stderr_msg)
                    return ExecutionStatus.CRASH, error_msg
                else:
                    return ExecutionStatus.EXCEPTION, error_msg
        else:
            if verbose:
                stdout_msg = output.stdout.decode("utf-8")
                print("stdout> ", stdout_msg)
            return ExecutionStatus.SUCCESS, ""

def validate_status_process(
    g_code, python="python", device="cpu", verbose=False, output_path=None
) -> (ExecutionStatus, str):
    with open("/tmp/tmp{}.py".format(CURRENT_TIME), "w") as f:
        f.write(g_code)
    # print("/tmp/tmp{}.py".format(CURRENT_TIME))
    run_args = [python, "/tmp/tmp{}.py".format(CURRENT_TIME)]
    print("----> output_path:", output_path)
    status, msg = run_cmd(run_args, verbose=verbose, cwd=output_path)
    return status, msg

def reask(dialog, extract_res, MAX_TRY, temperature, model):
    SUCCESS = 0
    try_cnt = 0
    while try_cnt < MAX_TRY:
        print("\n* try_cnt:", try_cnt)
        print("\n\n======================== dialog [start] ========================")
        for i in range(len(dialog)):
            line = dialog[i]
            role = line["role"]
            content = line["content"]
            print(f"=============>>>> {role}: {content}")
        print("======================== dialog [end]========================\n\n")


        raw_llm = llm_messages(model, dialog, temperature)
        res, valid = extract_res(raw_llm) 
        print("\n\n------------------------ raw_llm [start] ------------------------")
        print("** raw_llm:", raw_llm)
        print("\n\n------------------------ raw_llm [end] ------------------------")

        print("\n\n++++++++++++++++++++++++ extracted res [start] ++++++++++++++++++++++++")
        print("** extracted res:", res)
        print("\n\n++++++++++++++++++++++++ extracted res [end] ++++++++++++++++++++++++")

        if valid:
            SUCCESS = 1
            break
        else:
            dialog.append(
                {"role": "assistant", "content": raw_llm}
            )
            dialog.append(
                {"role": "user", "content": res + " Please generate again."}
            )

        try_cnt += 1
    
    if SUCCESS:
        return res
    else:
        print("* Can not finish this task. Here are the unsloved problem:", res)
        return None

def gen_code_debug(dialog, MAX_TRY, model, temperature):

    SUCCESS = 0
    try_cnt = 0
    while try_cnt < MAX_TRY:
        print("\n* try_cnt:", try_cnt)
        print("\n\n======================== dialog [start] ========================")
        for i in range(len(dialog)):
            line = dialog[i]
            role = line["role"]
            content = line["content"]
            print(f"=============>>>> {role}: {content}")
        print("======================== dialog [end]========================\n\n")

        raw_llm = llm_messages(model, dialog, temperature)
        res, valid = extract_res_for_code_gen(raw_llm)
        print("\n\n------------------------ raw_llm [start] ------------------------")
        print("** raw_llm:", raw_llm)
        print("\n\n------------------------ raw_llm [end] ------------------------")

        print("\n\n++++++++++++++++++++++++ extracted res [start] ++++++++++++++++++++++++")
        print("** extracted res:", res)
        print("\n\n++++++++++++++++++++++++ extracted res [end] ++++++++++++++++++++++++")

        if valid:
            SUCCESS = 1
            break
        else:
            dialog.append(
                {"role": "assistant", "content": raw_llm}
            )
            dialog.append(
                {"role": "user", "content": res + " Please generate again."}
            )
            print(res)

        try_cnt += 1
    
    if SUCCESS:
        return res, raw_llm
    else:
        print("Can not finish this task.")
        return None, None


library_need_to_be_installed = []
debug_cnt = {
    "successful": 0,
    "failed": 0
}

messages_feature = [
    {"role": "system", "content": "You are an expert in file structures, familiar with the characteristics and compositions of various file formats."},
    {"role": "user", "content": ""}
]
feature_prompt = """What features can '<TARGET>' files have? Output the information in the following format:

1. <feature 1>: <feature description>
2. <feature 2>: <feature description>
3. <feature 3>: <feature description>
......
N. <feature N>: <feature description>"""
feature_prompt_reask = """Here are some features associated with '<TARGET>' files:
<KNOWN_FEATURES>

Apart from the above features, what other features can '<TARGET>' files have? Output the information in the following format:

1. <feature 1>: <feature description>
2. <feature 2>: <feature description>
3. <feature 3>: <feature description>
......
N. <feature N>: <feature description>"""

messages_code_gen = [
    {"role": "system", "content": "You are an advanced Language Model assistant that can generate, execute, and evaluate code. Please use Markdown syntax to represent code blocks."},
    {"role": "user", "content": ""}
]
code_gen_prompt = """Generate '<TARGET>' files containing the following features using Python without any input files, and save the generated files into `./tmp/`.: 
```
<TARGET_FEATURES>
```
Please use Markdown syntax to represent code blocks. Please ensure that there is only one code block. You don't need to tell me which libraries need to be installed.
"""

def reask_for_feature(dialog, extract_res, MAX_TRY, model, temperature):
    SUCCESS = 0
    try_cnt = 0
    while try_cnt < MAX_TRY:
        print("\n* try_cnt:", try_cnt)
        print("\n\n======================== dialog [start] ========================")
        for i in range(len(dialog)):
            line = dialog[i]
            role = line["role"]
            content = line["content"]
            print(f"=============>>>> {role}: {content}")
        print("======================== dialog [end]========================\n\n")

        raw_llm = llm_messages(model, dialog, temperature)
        res, valid = extract_res(raw_llm) 
        print("\n\n------------------------ raw_llm [start] ------------------------")
        print("** raw_llm:", raw_llm)
        print("\n\n------------------------ raw_llm [end] ------------------------")

        print("\n\n++++++++++++++++++++++++ extracted res [start] ++++++++++++++++++++++++")
        print("** extracted res:", res)
        print("\n\n++++++++++++++++++++++++ extracted res [end] ++++++++++++++++++++++++")

        if valid:
            SUCCESS = 1
            break
        else:
            dialog.append(
                {"role": "assistant", "content": raw_llm}
            )
            dialog.append(
                {"role": "user", "content": res + " Please generate again."}
            )

        try_cnt += 1
    
    if SUCCESS:
        res_dict = {}
        for feature in res:
            pattern = r"(\d+)\.(.*?):"
            matches = re.findall(pattern, feature)
            if matches:
                res_dict[matches[0][1].strip()] = feature

        return res_dict, raw_llm
    else:
        print("* Can not finish this task. Here are the unsloved problem:", res)
        return None, raw_llm

def messages_for_feature(TARGET):
    prompt = feature_prompt.replace("<TARGET>", TARGET)

    messages = copy.deepcopy(messages_feature)
    messages[-1]["content"] = prompt
    
    return messages

def messages_for_feature_reask(TARGET, known_features):
    prompt = feature_prompt_reask.replace("<TARGET>", TARGET)
    prompt = prompt.replace("<KNOWN_FEATURES>", known_features)

    messages = copy.deepcopy(messages_feature)
    messages[-1]["content"] = prompt

    # prompt = feature_prompt_reask.replace("<TARGET>", TARGET)
    # messages.append({"role": "user", "content": prompt})
    
    return messages

def messages_for_code_gen(TARGET, TARGET_FEATURES):
    prompt = code_gen_prompt.replace("<TARGET>", TARGET)
    prompt = prompt.replace("<TARGET_FEATURES>", TARGET_FEATURES)

    messages = copy.deepcopy(messages_code_gen)
    messages[-1]["content"] = prompt
    
    return messages



generator_mutation_prompt = """
```
<TARGET_GENERATOR>
```

The code above is used to generate <FROMAT> files. Now, we need to extend this code to generate a new <FROMAT> file that includes an additional `<NEW_FEATURE>` feature besides the existing features. The description of the `<NEW_FEATURE>` feature is as follows:
```
<FEATURE_DES>
```

Please respond according to the following template: 
Here's an extended version of the code that generates a <FROMAT> file with an additional file feature `<NEW_FEATURE>`: 
```
<Generated Code>
```

Please use Markdown syntax to represent code blocks. Please ensure that there is only one code block. You don't need to tell me which libraries need to be installed.
"""

def messages_for_generator_mutation(file_format, feature, feature_description, target_generator_code):
    prompt = generator_mutation_prompt.replace("<FROMAT>", file_format)
    prompt = prompt.replace("<NEW_FEATURE>", feature)
    prompt = prompt.replace("<FEATURE_DES>", feature_description)
    prompt = prompt.replace("<TARGET_GENERATOR>", target_generator_code)

    messages = copy.deepcopy(messages_code_gen)
    messages[-1]["content"] = prompt
    
    return messages

def extract_res_for_code_gen(text):
    res = None
    valid = False

    count = 0
    modified_text = ""
    lines = text.split("\n")
    starts = []
    ends = []
    line_cnt = 0
    for line in lines:
        if line.startswith("```"):
            if count % 2 == 0:
                starts.append(line_cnt)
            else:
                ends.append(line_cnt)
            count += 1
        else:
            modified_text += line + "\n"
        
        line_cnt += 1
    
    if len(starts) == 0 and len(ends) == 0:
        msg = "There is no code block in the input text. Please use Markdown syntax to represent code blocks. Please ensure that there is only one code block."

        res = msg
        valid = False
    elif len(starts) != len(ends):
        msg = "The code blocks in the input text are not conforming to the Markdown syntax."
        
        res = msg
        valid = False
    elif len(starts) > 1:
        msg = "There are several code blocks in the input text. Please ensure that there is only one code block."
        
        res = msg
        valid = False

    if res:
        # did not generate the code block
        return res, valid
    
    res = "\n".join(lines[starts[0]+1:ends[0]])

    if "./tmp" not in res:
        msg = "You should save the generated files into `./tmp/`."

        res = msg
        valid = False
        return res, valid

    valid = True
    return res, valid

def extract_error_info(error_output):
    global library_need_to_be_installed

    # Extract additional error information, e.g., error line and error function
    # This is a basic example, and you might need to customize it based on your specific error format
    lines = error_output.split('\n')
    last_error_item = None
    error_function = None
    msg = None
    for cnt in range(len(lines)):
        
        line = lines[cnt]
        if "/tmp/tmp" in line.lower():
            # print("Error Line:", line.strip())
            # print("Error Function:", lines[cnt + 1].strip())
            error_function = lines[cnt + 1].strip()

        if 'error' in line.lower():
            last_error_item = line
    # print('Error info:', error_function)

    if error_function:
        msg = "Error Function: " + error_function + "\n"
        if last_error_item:
            msg += "Error Information: " + last_error_item.strip()

            if "ModuleNotFoundError" in last_error_item.strip():
                library_need_to_be_installed.append(last_error_item.strip())

    return msg


    
def display_code(codes):
    if not codes:
        return
    codes = codes.split('\n')
    print("++++++++++ code start ++++++++++")
    for line in codes:
        print("+ ", line)
    print("---------- code end ----------")


pip_debug_record = []

def extract_res_for_pip(text):
    res = None
    valid = False

    count = 0
    modified_text = ""
    lines = text.split("\n")
    starts = []
    ends = []
    line_cnt = 0
    for line in lines:
        if line.startswith("```"):
            if count % 2 == 0:
                starts.append(line_cnt)
            else:
                ends.append(line_cnt)
            count += 1
        else:
            modified_text += line + "\n"
        
        line_cnt += 1
    
    if len(starts) == 0 and len(ends) == 0:
        msg = "There is no code block in the input text. Please use Markdown syntax to represent code blocks. Please ensure that there is only one code block."

        res = msg
        valid = False
    elif len(starts) != len(ends):
        msg = "The code blocks in the input text are not conforming to the Markdown syntax."
        
        res = msg
        valid = False
    elif len(starts) > 1:
        msg = "There are several code blocks in the input text. Please ensure that there is only one code block."
        
        res = msg
        valid = False

    if res:
        # did not generate the code block
        return res, valid
    
    res = "\n".join(lines[starts[0]+1:ends[0]])

    if "pip" not in res:
        msg = "You should install the library via pip"

        res = msg
        valid = False
        return res, valid

    valid = True
    return res, valid

def pip_debug_loop(dialog, MAX_TRY, model, temperature):
    SUCCESS = 0
    try_cnt = 0
    while try_cnt < MAX_TRY:
        raw_llm = llm_messages(model, dialog, temperature)
        code, msg = extract_res_for_pip(raw_llm) 

        if code:
            SUCCESS = 1
            break
        else:
            dialog.append(
                {"role": "assistant", "content": raw_llm}
            )
            dialog.append(
                {"role": "user", "content": msg + " Please generate again."}
            )
            print(msg)

        try_cnt += 1
    
    if SUCCESS:
        return code, raw_llm
    else:
        print("Can not finish this task.")
        return None

def pip_debug(msg, MAX_TRY, model, temperature):
    global pip_debug_record

    install_flag = 0 # 0 represents installing failed, 1 represents installing successfully

    if msg in pip_debug_record: # indicate that has processed this msg before and failed to solved it. If we solved the msg successfully, we should not meet it again.
        return install_flag

    pip_debug_prompt_init = "```\n<MSG>\n```\nPlease use Markdown syntax to represent the command. Please ensure that there is only one command. To solve the above issue using Python's package manager pip, you should run the following command in the command-line interface:"
    pip_debug = [
        {"role": "system", "content": "You are an advanced Language Model assistant that can evaluate, execute, and debug code. Please use Markdown syntax to represent the command."},
    ]

    tmp = copy.deepcopy(pip_debug_prompt_init)
    tmp = tmp.replace('<MSG>', msg)
    pip_debug.append(
        {"role": "user", "content": tmp}
    )
    code, raw_llm = pip_debug_loop(pip_debug, MAX_TRY, model, temperature)

    # install library via pip
    print("You should install:", code)
    cmd = code.split()
    try:
        subprocess.check_call(cmd, timeout=120)
        install_flag = 1
        print(f"'{cmd}' successfully.")
    except subprocess.CalledProcessError:
        print(f"'{cmd}' failed.")

    pip_debug_record.append(msg)
    return install_flag

def self_debug(code, MAX_TRY, model, temperature = 0.2, output_path=None):
    global debug_cnt

    origin_code = code
    print("* original code:")
    display_code(origin_code)

    user_debug_init = "Fix the bug in the following code, described as '<BUG_DES>'.\n```python\n<CODE>\n```\n\nPlease use Markdown syntax to represent code blocks."
    user_debug = "The repaired code still has the following errors:'<BUG_DES>'"

    

    debug_template = [
        {"role": "system", "content": "You are an advanced Language Model assistant that can evaluate, execute, and debug code. Please use Markdown syntax to represent code blocks."},
    ]
    debug = copy.deepcopy(debug_template)

    
    # print("=== start ===")
    '''
        You can generate programs and execute them
    '''
    SUCCESS = 0
    try_cnt = 0
    while try_cnt < MAX_TRY:
        if try_cnt != 0: # need to reask llm to fix the bug
            print("\n* try_cnt:", try_cnt)
            print("** dialog ** [start]")
            for i in range(len(debug)):
                line = debug[i]
                role = line["role"]
                content = line["content"]
                print(f"*** {role}: {content}")
            print("** dialog ** [end]")

            # print(debug)
            # display(debug)
            code, raw_llm = gen_code_debug(debug, MAX_TRY, model, temperature)
            print("** repaired code:")
            display_code(code)
        
        if not code:
            break

        print("----> output_path:", output_path)
        status, msg = validate_status_process(code, output_path=output_path)
        valid = status == ExecutionStatus.SUCCESS


        # Debug Step I: solve the problems of dependency library
        if not valid:
            print("\n=== PIP Start ===")
            msg_tmp = extract_error_info(msg)
            if msg_tmp:
                msg = msg_tmp
            else:
                print("** We can not extract the error info for this msg:")
                print(msg)
                break
            
            library_dependecy_flag = 0
            while True:
                if "ModuleNotFoundError" not in msg:
                    library_dependecy_flag = 1
                    break
                
                flag = pip_debug(msg, MAX_TRY, model, temperature)
                if flag == 0: # we can not install the corresponding library
                    break
        
                # After install the dependency library, we rerun the program
                print("----> output_path:", output_path)
                status, msg = validate_status_process(code, output_path=output_path)
                valid = status == ExecutionStatus.SUCCESS

                if valid:
                    library_dependecy_flag = 1
                    break
                else:
                    msg_tmp = extract_error_info(msg)
                    if msg_tmp:
                        msg = msg_tmp
                    else:
                        print("** We can not extract the error info for this msg:")
                        print(msg)
                        break
            if library_dependecy_flag == 0: #indicate that we can not install dependency libraries properly. Thus, we just abort it.
                break
            print("=== PIP End ===\n")


        if valid:
            SUCCESS = 1
            break
        else:
            # msg_tmp = extract_error_info(msg)
            # if msg_tmp:
            #     msg = msg_tmp
            # else:
            #     print("---- We can not extract the error info for this msg:")
            #     print(msg)
            #     break
            print("** final msg:", msg)
            if try_cnt == 0:
                
                tmp = copy.deepcopy(user_debug_init)
                tmp = tmp.replace('<BUG_DES>', msg)
                tmp = tmp.replace('<CODE>', code)

                debug.append(
                    {"role": "user", "content": tmp}
                )
            else:
                debug.append(
                    {"role": "assistant", "content": raw_llm}
                )

                tmp = copy.deepcopy(user_debug)
                tmp = tmp.replace('<BUG_DES>', msg)
                debug.append(
                    {"role": "user", "content": tmp + " Please generate again."}
                )
        try_cnt += 1
    
    if SUCCESS:
        print("* SUCCESS")
        if try_cnt != 0:
            debug_cnt["successful"] += 1
            print("** You have repaired the program successfully!!!")
            # print("\n=== debug start ===")
            # print("--> origin_code:")
            # print(origin_code)
            # print("\n--> current code:")
            # print(code)
            # print("=== debug end ===\n")
        return code
    else:
        debug_cnt["failed"] += 1
        print("* Can not finish this task.")
        return None

def mv_files(source_dir, target_dir, file_prefix):
    # 定义大小限制为10MB
    size_limit = 10 * 1024 * 1024  # 10MB = 10 * 1024 * 1024 bytes

    cnt = 1
    for filename in os.listdir(source_dir):
        source_path = os.path.join(source_dir, filename)

        # 检查文件大小，如果大于10MB，则删除该文件
        if os.path.getsize(source_path) > size_limit:
            os.remove(source_path)
            print(f"---- Deleted large file {source_path} (greater than 10MB)")
            continue  # 跳过该文件，避免继续移动

        target_path = os.path.join(target_dir, file_prefix + "_" + str(cnt) + os.path.splitext(filename)[1])
        cnt += 1
        
        # 移动文件
        shutil.move(source_path, target_path)
        print(f"---- Moved {source_path} to {target_path}")

def count_files_in_directory(path):
    count = 0
    for _, _, files in os.walk(path):
        count += len(files)
    return count

def get_file_format(seeds_list):
    seeds_list = [s for s in seeds_list if s.count('.') == 1]
    file_extensions = [file_name.split('.')[-1] for file_name in seeds_list]
    extension_counts = Counter(file_extensions)
    max_extensions = extension_counts.most_common(6)
    extension_names = [extension[0] for extension in max_extensions]
    return extension_names

def extract_res_for_feature(raw_llm):
    feature_pool = match_res_for_feature(raw_llm)

    if feature_pool:
        res = feature_pool
        valid = True
        return res, valid
    else:
        res = """You did not output in the given format. Output the information in the following format:

1. <feature 1>: <feature description>
2. <feature 2>: <feature description>
3. <feature 3>: <feature description>
......
N. <feature N>: <feature description>"""
        valid = False
        return res, valid

def match_res_for_feature(text):
    feature_pool = []
    features_lines = text.strip().split('\n')
    for line in features_lines:
        pattern = r"(\d+)\.(.*?):"
        matches = re.findall(pattern, line)        

        if matches:
            feature_pool.append(line)
    return feature_pool
