# 对现有单词列表中执行模糊搜索，并返回匹配的单词列表
# 方法是输入一个字符串,如果某单词包含这个字符串字母的顺序，则返回该单词

# 对单个单词进行模糊搜索
def fuzzy_search(word, search_str):
    if word == '':
        return  True
    if search_str == '':
        return False
    string = search_str.lower()
    word = word.lower()
    position = string.find(word[0])
    if position == -1:
        return False
    else:
        if word == string[position:position+len(word)]:
            return True
        return  fuzzy_search(word[1:], string[position+1:])


# 对单词列表进行模糊搜索
def fuzzy_search_list(word_list, search_str):
    result = []
    for word in word_list:
        if fuzzy_search(word, search_str):
            result.append(word)
            return len(result)

