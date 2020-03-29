import os

folder_path = "/Users/hzguo/11785/group/dataverse_files/staple-2020-train/en_hu"

gold_file = folder_path + "/" +"train.en_hu.2020-01-13.gold.txt"
baseline_file = folder_path + "/" + "train.en_hu.aws_baseline.pred.txt"

output_folder = "/Users/hzguo/11785/group/en_hu"

train_folder = output_folder + "/" + "train" + "/"
test_folder = output_folder + "/" + "test" + "/"
val_folder = output_folder + "/" + "val" + "/"


train_prop = 0.9

try:
    os.mkdir(train_folder)
    os.mkdir(test_folder)
    os.mkdir(val_folder)
except :
    pass

prompt_dict = {}

prompt_id = None

max_list_length = 0

with open(gold_file, "r") as f1, open(baseline_file, "r") as f2:
    for line in f1:
        if len(line) == 1:
            if prompt_id is not None:
                prompt_dict[prompt_id] = [prompt_text, prompt_accept]
                max_list_length = max(max_list_length, len(prompt_accept))
            prompt_id = None
            continue

        if prompt_id is None:
            parts = line.split("|")
            prompt_id = parts[0]
            prompt_text = parts[1][:-1]
            prompt_accept = []
        else:
            parts = line.split("|")
            prompt_accept.append((parts[0], float(parts[1])))

    if prompt_id is not None:
        prompt_dict[prompt_id] = [prompt_text, prompt_accept]
    prompt_id = None
    for line in f2:
        if len(line) == 1:
            prompt_id = None
            continue

        if prompt_id is None:
            parts = line.split("|")
            prompt_id = parts[0]
            prompt_text = parts[1][:-1]
            assert(prompt_text == prompt_dict[prompt_id][0])
        else:
           prompt_dict[prompt_id].append(line)

prompt_id_list = [k for k in prompt_dict.keys()]
train_number = int(len(prompt_id_list)*train_prop)
train_prompt_id_list = prompt_id_list[:train_number]
test_prompt_id_list = prompt_id_list[train_number:]


def write_train_file(folder_name, prompt_id_list):
    with open(folder_name + "src.txt", "w") as f1, open(folder_name + "tgt.txt", "w") as f2:
        for i in range(int((max_list_length+1)/2)):
            for prompt_id in prompt_id_list:
                id0 = 2*i
                id1 = 2*i+1
                if id1-1 < len(prompt_dict[prompt_id][1]):
                    f1.write(prompt_dict[prompt_id][2] if id0 == 0 else prompt_dict[prompt_id][1][id0-1][0] + "\n")
                    f2.write(prompt_dict[prompt_id][1][id1-1][0] + "\n")


def write_test_file(folder_name, prompt_id_list):
    with open(folder_name + "src.txt", "w") as f1, open(folder_name + "tgt.txt", "w") as f2:
        for prompt_id in prompt_id_list:
            f1.write("{}|{}".format(prompt_id,prompt_dict[prompt_id][2]))
            f2.write("{}|{}\n".format(prompt_id,prompt_dict[prompt_id][0]))
            for line in prompt_dict[prompt_id][1]:
                f2.write("{}|{}\n".format(line[0], line[1]))
            f2.write("\n")


write_train_file(train_folder, train_prompt_id_list)
write_train_file(val_folder, test_prompt_id_list)
write_test_file(test_folder, test_prompt_id_list)







