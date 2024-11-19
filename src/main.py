import json
import random
from tools import fuzzy_search


#执行需要听写的单词的录入
def logging_data():
    # 录入单词及其翻译
    print("输入exit退出")
    with open('word.json', 'r', encoding='utf-8') as f:
        word = json.load(f)
    while True:
        word_input = input("请输入单词：")
        if word_input == 'exit':
            break
        else:
            word_translation = input("请输入单词的翻译：")
            word[word_input] = word_translation
    with open('word.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(word, ensure_ascii=False,indent=2))
    print("单词及其翻译已保存！")

# 修改单词的翻译
def modify_translation():
    with open('word.json', 'r', encoding='utf-8') as f:
        word = json.load(f)
    print("输入exit退出")
    while True:
        word_input = input("请输入需要修改的单词")
        if word_input == 'exit':
            break
        else:
            if word_input in word:
                print("当前翻译：", word[word_input])
                word_translation = input("请输入新的翻译：")
                word[word_input] = word_translation
                with open('word.json', 'w', encoding='utf-8') as f:
                    f.write(json.dumps(word, ensure_ascii=False))
                print("单词翻译已修改！")
            else:
                print("单词不存在！")

# 单词录入错误时,删除单词,并重新录入
def delete_word():
    print("输入exit退出")
    with open('word.json', 'r', encoding='utf-8') as f:
        word = dict(json.load(f))
        print(type(word))
    while True:
        word_input = input("请输入需要删除的单词")
        if word_input == 'exit':
            return
        else:
            # 进行模糊匹配,找到与输入单词相似的单词,并标上序号以供选择
            similar_words = []
            for key in word.keys():
                if fuzzy_search(word_input, key):
                    similar_words.append(key)
            if similar_words:
                print("找到以下相似的单词：")
                for i, sword in enumerate(similar_words):
                    print(i+1, sword)
                choice = int(input("请输入需要删除的单词序号："))
                if choice <= len(similar_words):
                    print(type(word))
                    word.pop(similar_words[choice-1])
                    with open('word.json', 'w', encoding='utf-8') as f:
                        f.write(json.dumps(word, ensure_ascii=False,indent=2))
                    print("单词已删除！")
                    # 选择是否重新录入
                    choice = input("是否重新录入？(y/n)")
                    if choice == 'y':
                        logging_data()
                    elif choice == 'n':
                        print("已退出！")
                    else:
                        print("输入错误！")

                else:
                    print("序号输入错误！")
            else:
                print("单词不存在！")

#对单个单词进行听写,通过则返回True,否则返回False,则需要加入错词本
def listening_word(word_key, word_translation):
    while True:
        print("翻译：", word_translation)
        user_input = input("请输入正确的单词：")
        if user_input == word_key:
            return True
        elif user_input == 'exit':
            raise Exception("退出本次听写！")
        else:
            print("回答错误！")
            # 选择尝试再次输入单词还是把该词加入错词本
            while True:
                choice = input("是否尝试再次输入？(y/n/exit)")
                if choice == 'y':
                    return listening_word(word_key, word_translation)
                elif choice == 'n':
                    return True
                elif choice == 'exit':
                    raise Exception("退出本次听写！")
                else:
                    print("输入错误！")


# 执行听写程序,随机选择单词翻译打印在终端,并提示用户输入正确的单词
def listening_program(word=None):

    # 记录已经听写的单词
    listened_words = []
    # 错词本
    error_words = []

    # 如果没有传入单词字典,则从文件中读取
    if not word:
        with open('word.json', 'r', encoding='utf-8') as f:
            word = json.load(f)
    try:
        while True:
            # 随机选择一个单词
            word_key = random.choice(list(word.keys()))
            word_translation = word[word_key]
            # 打印单词及其翻译
            print("翻译：", word_translation)
            # 等待用户输入正确的单词
            if listening_word(word_key, word_translation):
                print("回答正确！")
                # 记录听写的单词
                listened_words.append(word_key)
                # 删除已听写的单词
                word.pop(word_key)
                if not word:
                    print("全部单词听写完毕！")
                    return
                listening_program(word)
            else:
                print("回答错误！")
                # 选择尝试再次输入单词还是把该词加入错词本
                while True:
                    choice = input("是否尝试再次输入？(y/n/e)")
                    if choice == 'y':
                        result = listening_word(word_key, word_translation)
                        if result:
                            print("回答正确！")
                            listened_words.append(word_key)
                            word.pop(word_key)
                            if not word:
                                print("全部单词听写完毕！")
                                return
                            listening_program(word)
                        else:
                            print("回答错误！")
                    elif choice == 'e':
                        error_words.append(word_key)
                    elif choice == 'n':
                        error_words.append(word_key)
                        break
                    elif choice == 'e':
                        error_words.append(word_key)
                        #打印错词本并退出
                        print("错词本：", error_words)
                        with open('error_word.json', 'w', encoding='utf-8') as f:
                            f.write(json.dumps(error_words, ensure_ascii=False,indent=2))
                        print("错词本已保存！")
                        return
                    else:
                        print("输入错误！")
    except:
        return


# 单词助记功能
def word_memory():
    print("欢迎使用单词助记功能！")
    print("提示:输入 exit 退出助记功能")
    # 读取单词及其翻译
    with open('word.json', 'r', encoding='utf-8') as f:
        word = json.load(f)
    # 随机选择一个单词打印单词及其翻译
    while True:
        word_key = random.choice(list(word.keys()))
        word_translation = word[word_key]
        print(f"单词：{word_key}, 翻译：{word_translation}")
        # 用户再次输入单词,输入exit退出助记功能,如果输错则提示重新输入
        while True:
            user_input = input("请输入单词：")
            if user_input == 'exit':
                print("退出助记功能！")
                return
            elif user_input == word_key:
                print("下一个是:")
                word.pop(word_key)
                if not word:
                    print("全部单词助记完毕！")
                    print("5秒后退出助记功能！")
                    import time
                    time.sleep(5)
                    return
                break
            elif user_input != word_key:
                print("输入错误！,在输一遍吧")







def main():
    # 选择功能
    while True:
        print("1. 听写单词")
        print("2. 录入单词及其翻译")
        print("3. 修改单词的翻译")
        print("4. 删除单词")
        print("5. 单词助记")
        print("exit 退出")
        choice = input("请输入功能序号：")
        if choice == '1':
            listening_program()
        elif choice == '2':
            logging_data()
        elif choice == '3':
            modify_translation()
        elif choice == '4':
            delete_word()
        elif choice == '5':
            word_memory()
        elif choice == 'exit':
            return
        else:
            print("输入错误！")

if __name__ == '__main__':
    main()
