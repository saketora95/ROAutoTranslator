def read_compare_file(file_path):
    open_file = open(file_path, 'r', encoding='utf-8-sig')
    raw_data = open_file.readlines()
    open_file.close()

    return build_compare_data(raw_data)

def build_compare_data(raw_data):
    data_dict = {}
    for line in raw_data:
        if line == '\n' or line[0] == '#':
            pass

        else:
            if ' = ' in line:
                line = line[:-1].split(' = ')
                line_length = len(line[0])

                if line_length in data_dict:
                    data_dict[line_length][line[0]] = line[1]
                
                else:
                    data_dict[line_length] = {}
                    data_dict[line_length][line[0]] = line[1]

    dict_length = []
    for length in data_dict:
        dict_length.append(length)
    
    dict_length = sorted(dict_length, reverse=True)

    sort_data_dict = {}
    for length in dict_length:
        sort_data_dict[length] = data_dict[length].copy()

    return sort_data_dict

def compare_string(target, data_dict):
    for length in data_dict:
        for word in data_dict[length]:
            if word in target:
                target = target.replace(word, data_dict[length][word])

    return target