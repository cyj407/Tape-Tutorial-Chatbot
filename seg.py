#encoding=utf-8
import jieba

jieba.set_dictionary("./dict.txt.big")


def seg_word(sentence):
    seg_list = jieba.cut(sentence)
    return seg_list