import collections
import jieba


class DictAnalysis:
    def __init__(self, text_type):
        # 初始化情感词字典、否定词列表与程度副词词典
        self.sentiment_dict = collections.defaultdict()
        self.not_word_list = []
        self.degree_dict = []

        # 读取情感词典文件
        if text_type == 'news':
            sen_file = open("./dict/financial_sentiment_score.txt", "r+", encoding="utf-8")
        else:
            sen_file = open("./dict/BosonNLP_sentiment_score.txt", "r+", encoding="utf-8")
        sen_list = sen_file.readlines()
        # 创建情感字典
        for i in sen_list:
            if len(i.split(' ')) == 2:
                self.sentiment_dict[i.split(" ")[0]] = i.split(" ")[1].strip()

        # 读取否定词
        not_word_file = open("./dict/否定词.txt", "r", encoding="utf-8")
        self.not_word_list = not_word_file.readlines()
        self.not_word_list = [wo.strip() for wo in self.not_word_list]

        # 读取程序副词
        degree_file = open("./dict/程度副词.txt", "r", encoding="utf_8")
        degree_list = degree_file.readlines()
        self.degree_dict = collections.defaultdict()
        for i in degree_list:
            self.degree_dict[i.split(",")[0]] = i.split(",")[1].strip()

        sen_file.close()
        not_word_file.close()
        degree_file.close()

    # 使用jieba分词并去除停用词
    @staticmethod
    def seg_word(sentence):
        seg_list = jieba.cut(sentence)
        seg_result = []
        for i in seg_list:
            seg_result.append(i)
        stopwords = set()
        with open("./dict/新停用词.txt", "r", encoding="utf-8") as f:
            for i in f:
                stopwords.add(i.strip())
        return list(filter(lambda x: x not in stopwords, seg_result))

    # 对已分词的句子进行词词语分类
    def classify_word(self, word_list):

        # 分类结果，词语索引为key，分值为value，否定词分值为-1
        sen_word = dict()
        not_word = dict()
        degree_word = dict()

        # 分类
        for word in word_list:
            if word in self.sentiment_dict.keys() \
                    and word not in self.not_word_list \
                    and word not in self.degree_dict.keys():
                # 找出分词结果中在情感字典中的词
                sen_word[word] = self.sentiment_dict[word]
            elif word in self.not_word_list \
                    and word not in self.degree_dict.keys():
                # 分词结果中在否定词列表中的词
                not_word[word] = -1
            elif word in self.degree_dict.keys():
                # 分词结果中在程度副词中的词
                degree_word[word] = self.degree_dict[word]
        # 将分类结果返回
        # 词语索引为key，分值为value，否定词分值为 - 1
        return sen_word, not_word, degree_word

    # 计算情感分数
    @staticmethod
    def cal_score(sen_word, not_word, degree_word, seg_result):
        # 权重初始化为1
        weight = 1
        score = 0
        # 遍历分词结果
        for i in range(0, len(seg_result)):
            # 若是程度副词
            if seg_result[i] in degree_word.keys():
                weight = (weight / weight * float(degree_word[seg_result[i]]))
                # weight *= float(degree_word[seg_result[i]])
            # 若是否定词
            elif seg_result[i] in not_word.keys():
                weight *= -1
            elif seg_result[i] in sen_word.keys():
                score += float(weight) * float(sen_word[seg_result[i]])
                weight = 1
        return score

    # 总计算流程
    def sentiment_score(self, sentence):
        seg_result = self.seg_word(sentence)
        sen_word, not_word, degree_word = self.classify_word(seg_result)
        score = self.cal_score(sen_word, not_word, degree_word, seg_result)
        return score

    # 计算总体分数
    def cal_total_score(self, path):
        DA = DictAnalysis('news')
        pos_num = 0
        neg_num = 0
        f = open(path, encoding="utf-8")
        total_txt = f.readlines()

        for line in total_txt:
            print(line)
            score = DA.sentiment_score(line)
            print(score)
            if score > 0:
                pos_num = pos_num + 1
            if score < 0:
                neg_num = neg_num + 1
        print('正面情绪语句数量：{}'.format(pos_num))
        print('负面情绪语句数量：{}'.format(neg_num))
        print('正面情绪所占比例：{}'.format(pos_num / (pos_num + neg_num)))
        print('文本情感评分：{}'.format(pos_num / (pos_num + neg_num)))


# if __name__ == '__main__':
#     DA = DictAnalysis('news')
#     # 计算总体情感分数
#     path = '../test_data/test2.txt'
#     DA.cal_total_score(path)
