input_file_name = 'data/quora/test/src.txt'
output_file_name = 'data/quora/test/src_id.txt'

i = 0
with open(input_file_name, "r") as f, open(output_file_name, "w") as f2 :
    for line in f:
        f2.write("prompt_{}|{}".format(i,line))
        i+=1