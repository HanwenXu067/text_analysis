import jieba as ja
import jieba.posseg as seg
from snownlp import SnowNLP

with open("./test_data/test2.txt", encoding="utf-8") as f:
    analysis_test = f.read()
    print(analysis_test)

analysis_list = list(ja.cut(analysis_test))
print(analysis_list)
print('-----------------------------------')
analysis_words = [(word.word,word.flag)for word in seg.cut(analysis_test)]
print(analysis_words)
print('-----------------------------------')

# 提取关键字和关键字对应的词性
keywords = [x for x in analysis_words if x[1] in ['a','d','v']]
print(keywords)

# 去除情感标记，只保留关键字
keywords = [x[0] for x in keywords]
print(keywords)

# 分词工作处理完，使用snownlp进行情感分析
pos_num = 0
neg_num = 0

for word in keywords:
    s1 = SnowNLP(word)
    if s1.sentiments > 0.5:
        pos_num = pos_num + 1
    else:
        neg_num = neg_num + 1
    print(word,str(s1.sentiments))

# 对正面及负面关键词进行统计得到一个结果
print('正面情绪关键词数量：{}'.format(pos_num))
print('负面情绪关键词数量：{}'.format(neg_num))
print('正面情绪所占比例：{}'.format(pos_num/(pos_num + neg_num)))
