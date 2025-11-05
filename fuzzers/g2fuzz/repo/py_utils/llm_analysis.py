from .llm_utils import llm
import os
import multiprocessing
from tqdm import tqdm

def load_prompts_from_folder(source_folder):
    prompts = []
    filenames = os.listdir(source_folder)
    for filename in filenames:
        file_path = os.path.join(source_folder, filename)
        with open(file_path, 'r') as file:
            prompt = file.read()
            prompts.append((filename, prompt))
    return prompts

def save_responses_to_folder(responses, target_folder):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    for filename, response in responses:
        target_file_path = os.path.join(target_folder, filename)
        with open(target_file_path, 'w') as file:
            file.write(response)


def worker(params):
    """处理单个任务并捕获异常"""
    try:
        # 假设llm函数接收多个参数，params是参数元组
        result = llm(*params)
        return (True, result)
    except Exception as e:
        return (False, str(e))

def save_response_to_file(filename, response, folder):
    """将单个结果保存到文件"""
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, f"{filename}")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(response)

def process_in_batches(args, target_prompts, responses_folder, processes_num=10):
    """分批处理任务并定期保存"""
    processed_results = []
    
    try:
        with multiprocessing.Pool(processes=processes_num) as pool:
            results_iter = pool.imap(worker, args)
            
            # 使用tqdm创建进度条
            with tqdm(total=len(args), desc="Processing") as pbar:
                for idx, (success, result) in enumerate(results_iter):
                    filename = target_prompts[idx][0]
                    if success:
                        processed_results.append((filename, result))
                        # 实时保存每个结果
                        save_response_to_file(filename, result, responses_folder)
                    else:
                        print(f"Error processing {filename}: {result}")
                    
                    # 更新进度条
                    pbar.update(1)
                    
                    # 定期保存批次结果（可选，若需要批量保存可取消注释）
                    # if (idx + 1) % batch_size == 0:
                    #     save_responses_to_folder(processed_results, responses_folder)
                    
    except KeyboardInterrupt:
        print("\n用户中断！已保存当前处理的所有结果。")
    except Exception as e:
        print(f"\n发生未知错误: {e}，已保存当前处理的所有结果。")
    finally:
        # 最终保存所有已处理结果（如果使用批量保存）
        # save_responses_to_folder(processed_results, responses_folder)
        print(f"处理完成。结果保存在目录：{responses_folder}")

def run_prompts_parallelly(model, prompts_path, responses_folder, reasoning_effort, cost_file_path, processes_num):
    # Feed the prompts into LLMs
    prompts = load_prompts_from_folder(prompts_path)
    target_prompts = []
    args = []
    for filename, prompt in prompts:
        if os.path.exists(os.path.join(responses_folder, filename)):
            # print(f"Skipping {filename} as it already exists in the target folder.")
            continue
        target_prompts.append((filename, prompt))
        args.append((model, prompt, reasoning_effort, cost_file_path))

    
    # print("===== start =====")
    process_in_batches(args, target_prompts, responses_folder, processes_num)

if __name__ == "__main__":
    prompts_path = "./transfer_prompts"
    responses_folder = "./transfer_prompts_responses"
    reasoning_effort = "high"
    cost_file_path = "./cost.txt"
    model = "o3-mini"
    processes_num = 20
    run_prompts_parallelly(model, prompts_path, responses_folder, reasoning_effort, cost_file_path, processes_num)
    