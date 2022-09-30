import jieba
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pandas as pd


def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        message += " ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)
    print()

""" da """
def top_words(model, feature_names, n_top_words):
    message1 = []
    for topic_idx, topic in enumerate(model.components_):
        # message = "Topic #%d: " % topic_idx
        # message += " ".join([feature_names[i]
        #                      for i in topic.argsort()[:-n_top_words - 1:-1]])
        # print(message)
        message1.append(" ".join([feature_names[i]
                                  for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()
    return message1

class LDAClustering():
    def load_stopwords(self, stopwords_path):
        with open(stopwords_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f]

    def cut_words(self, sentence):
        return ' '.join(jieba.lcut(sentence))

    def pre_process_corpus(self, corpus_path, stopwords_path):
        """
        数据预处理，将语料转换成以词频表示的向量。
        :param corpus_path: 语料路径，每条语料一行进行存放
        :param stopwords_path: 停用词路径
        :return:
        """
        with open(corpus_path, 'r', encoding='utf-8') as f:
            corpus = [self.cut_words(line.strip()) for line in f]

        stopwords = self.load_stopwords(stopwords_path)

        self.cntVector = CountVectorizer(stop_words=stopwords)

        cntTf = self.cntVector.fit_transform(corpus)

        return cntTf

    def fmt_lda_result(self, lda_result):
        ret = {}
        for doc_index, res in enumerate(lda_result):
            li_res = list(res)
            doc_label = li_res.index(max(li_res))
            if doc_label not in ret:
                ret[doc_label] = [doc_index]
            else:
                ret[doc_label].append(doc_index)
        return ret

    def lda(self, corpus_path, n_components=5, learning_method='batch',
            max_iter=10, stopwords_path='../data/stop_words.txt'):
        """
        LDA主题模型
        :param corpus_path: 语料路径
        :param n_topics: 主题数目
        :param learning_method: 学习方法: "batch|online"
        :param max_iter: EM算法迭代次数
        :param stopwords_path: 停用词路径
        :return:
        """
        cntTf = self.pre_process_corpus(corpus_path=corpus_path, stopwords_path=stopwords_path)
        tf_feature_names = self.cntVector.get_feature_names_out()
        lda = LatentDirichletAllocation(n_components=n_components, max_iter=max_iter, learning_method=learning_method)
        docres = lda.fit_transform(cntTf)

        print_top_words(lda, tf_feature_names, n_top_words=10)
        topic_words = top_words(lda,tf_feature_names, n_top_words=10)
        return self.fmt_lda_result(docres),docres,topic_words

'''
lda = LatentDirichletAllocation(n_topics=5)
lda.fit(docres)
# predict topics for test data
# unnormalized doc-topic distribution
X_test = tf_vectorizer.transform(test)
doc_topic_dist_unnormalized = np.matrix(lda.transform(X_test))
'''
if __name__ == '__main__':
    LDA = LDAClustering()
    # ret,docres = LDA.lda('..\data\\tcad.txt', stopwords_path='..\data\stop_words2.txt', max_iter=100, n_components=5)
    # ret,docres = LDA.lda('..\data\opc.txt', stopwords_path='..\data\stop_words2.txt', max_iter=100, n_components=8)
    ret,docres = LDA.lda('..\data\good_rate.txt', stopwords_path='..\data\stop_words2.txt', max_iter=100, n_components=8)
    print(ret)

# ####将字典形式转化成数据形式
# def to_data(text,dicted):
#     se = pd.DataFrame()
#     tech = []
#     label = []
#     for i,j in dicted.items():
#         for l in j:
#             label.append(i)
#             tech.append(text[l])
#     se['tech'] = tech
#     se['label'] = label
#     se['text'] = text
#     return se
# sk = pd.read_excel('/Users/wangmujie/Desktop/空间研究所实习/lda/OPC_data_0924.xlsx')
# dict0 = {0:'image gif id he',1:'区域 模型 网格 缺陷 版图',2:'光学 fpga 连接 参数 节点',3:'模型 光学 信息 计算 图形',4:'模块 仿真 数据 仿真器 芯片',5:'目标 设备 光学 操作 信息',6:'模型 函数 目标 参数 节点',7:'参数 数据 模块 车辆 检测',8:'文件 安装 升级 信息 更新',9:'透镜 测量 矩阵 零件 装配'}
# rdata = to_data(sk['primary_right'],ret)
# rdict0 = rdata['label'].map(dict0)
# rdata['label'] = rdict0
# rdata