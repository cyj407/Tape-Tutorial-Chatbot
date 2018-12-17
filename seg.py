#encoding=utf-8
import jieba
import jieba.posseg as pseg

# 設定為繁中字典
jieba.set_dictionary("./dict.txt.big")


def seg_word(sentence):
    seg_list = jieba.cut(sentence)
    return seg_list

def seg_noun_word(sentence):
    noun_list = []
    seg_list = pseg.cut(sentence)
    for w in seg_list:
        if w.flag in "n":
            noun_list.append(w.word)
    return noun_list
