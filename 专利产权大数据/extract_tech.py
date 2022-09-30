import pandas as pd
import extract_Tech_wmj.extract_event as ee
import connection
import extract_Tech_wmj.LDA_classify as lda
import numpy as np
# eda = pd.read_excel('/Users/wangmujie/Desktop/空间研究所实习/功效技术点提取/opc_TCAD_rate.xlsx')
conn = connection.conn
sql = 'select * from eda20yall_filter where first_category is not null'
cursor = conn.cursor()
cursor.execute(sql)
# conn.commit()
data = cursor.fetchall()
des = cursor.description
columns_names = [des[i][0] for i in range(len(des))]

idx = [i for i in range(len(data))]
eda = pd.DataFrame(list(data), columns=des, index=idx)
# print(eda.iloc[0])
handler = ee.ExtractEvent()
# none_im = ['应用','方法','系统','介质','终端']
##改进策略 名词+动词
se = pd.DataFrame(columns=['发明名称', '技术点', '切分后', '专利申请号', '专利申请人','主权项','一级分类', '二级分类'], index=idx)
# se = []

se['发明名称']= eda['patent_title']
se['专利申请号'] = eda['patent_app_nu']
se['专利申请人'] = eda['patent_app_person']
se['主权项'] = eda['primary_right']
se['一级分类']  = eda['first_category']
se['二级分类']  = eda['second_category']
# se.columns = ['发明名称']
print(se.iloc[2]['发明名称'])
# se['技术点'] = None
# se['专利申请号'] = None
# for j in range(len(eda['patent_title'])-1):
#     se.iloc[j]['发明名称'] = ''.join(eda.iloc[j]['patent_title'].values)
res = []
sen_end = ['装置', '设备', '应用', '方法', '系统', '介质', '终端']
# eda = pd.read_excel('/Users/wangmujie/Desktop/空间研究所实习/功效技术点提取/opc_TCAD_rate.xlsx')

# none_im = ['应用','方法','系统','介质','终端']
##改进策略 名词+动词
#######从标题提取领域
se = pd.DataFrame()

# se['领域点'] = None
res = []
for m in range(len(TCAD['patent_title'])):
    res = []
    lead = 0
    i = se.loc[m]['发明名称']
    if '基于' in i and '的' in i:  # no problem
        k = i.find('基于')
        j = i.rfind('的')
        words, postags = handler.cut_wds(i[j + 1:])
        words, postags = handler.cut_wds(i[k + 2:j])
        if 'v' in postags:
            if postags.index('v') == 0 or postags.index('v') == 1:
                wp = words[postags.index('v')]
                lead = 1
        elif 'd' in postags:
            if postags.index('d') == 0 or postags.index('d') == 1:
                wp = words[postags.index('d')]
                lead = 1
        if len(words) == 1:
            res.append(i[k + 2:])
        elif lead == 1:
            res.append(i[k + 2:j] + wp)
        else:
            res.append(i[k + 2:j])

    elif i.find('使用') == 1 or i.find('使用') == 0:
        k = i.find('使用')
        if '的' in i:
            s = i.rfind('的')
            if len(i[k + 2:s]) <= 2:
                res.append(i[k + 2:s])
            else:
                res.append(i[k + 2:s])
        else:
            res.append(i[k + 2:])

    elif '用于' in i and '的' in i:  # problem less
        k = i.find('用于')
        j = i.find('的')
        words, postags = handler.cut_wds(i[j + 1:])

        if 'v' in postags:
            if postags.index('v') == 0 or postags.index('v') == 1:
                wp = words[postags.index('v')]
                lead = 1
        elif 'd' in postags:
            if postags.index('d') == 0 or postags.index('d') == 1:
                wp = words[postags.index('d')]
                lead = 1

        if lead == 1:
            res.append(i[k + 2:j] + wp)
        else:
            res.append(i[k + 2:j])

    elif '用于' in i and '之' in i:  # maybe problem
        k = i.find('用于')
        j = i.find('之')
        if 'v' in postags:
            if postags.index('v') == 0 or postags.index('v') == 1:
                wp = words[postags.index('v')]
                lead = 1
        elif 'd' in postags:
            if postags.index('d') == 0 or postags.index('d') == 1:
                wp = words[postags.index('d')]
                lead = 1

        if lead == 1:
            res.append(i[k + 2:j] + wp)
        else:
            res.append(i[k + 2:j])

    elif '针对' in i and '的' in i:
        k = i.find('针对')
        j = i.rfind('的')
        if len(i[j + 1:]) <= 3:
            res.append(i[k + 2:j])
        elif i[j + 1:j + 3] in sen_end or i[j + 2:j + 4] in sen_end or i[j + 3:j + 5] in sen_end:
            res.append(i[k + 2:j])
        #            i[j+1:j+3] in sen_end:
        else:
            res.append(i[j + 1:])
    elif i[0] == '对' and '的' in i:
        k = i.find('对')
        j = i.rfind('的')
        if len(i[j + 1:]) <= 3:
            res.append(i[k + 1:j])
        elif i[j + 1:j + 3] in sen_end or i[j + 2:j + 4] in sen_end or i[j + 3:j + 5] in sen_end:
            res.append(i[k + 1:j])
        #            i[j+1:j+3] in sen_end:
        else:
            res.append(i[j + 1:])

    elif '带有' in i and '的' in i:
        k = i.find('带有')
        j = i.find('的')
        if len(i[j + 1:]) <= 3:
            res.append(i[k + 2:j])
        elif i[j + 1:j + 3] in sen_end or i[j + 2:j + 4] in sen_end or i[j + 3:j + 5] in sen_end or i[-2:len(
                i)] in sen_end:
            res.append(i[k + 2:j])
        #            i[j+1:j+3] in sen_end:
        else:
            res.append(i[k + 2:j])


    elif '作为' in i and '的' in i:  #####many problem
        k = i.find('作为')
        j = i.find('的')
        if len(i[j + 1:]) <= 3:
            res.append(i[k + 2:j])
        elif i[j + 1:j + 3] in sen_end or i[j + 2:j + 4] in sen_end or i[j + 3:j + 5] in sen_end or i[-2:len(
                i)] in sen_end:
            res.append(i[k + 2:j])
        #            i[j+1:j+3] in sen_end:
        else:
            words, postags = handler.cut_wds(i[j + 1:])
            if 'v' in postags and 'n' in postags:
                res.append(i[j + 1:])
            else:
                res.append(i[k + 2:j])


    elif '通过' in i and '而' in i:  # many problem 利用L-EDA筛选卵巢癌体液预后标记物的方法
        k = i.find('通过')
        j = i.find('而')
        res.append(i[j + 1:])
    elif '通过' in i and '的' in i:  # many problem 利用L-EDA筛选卵巢癌体液预后标记物的方法
        k = i.find('通过')
        j = i.find('的')
        if len(i[j + 1:]) <= 3:
            res.append(i[k + 2:j])
        elif i[j + 1:j + 3] in sen_end or i[j + 2:j + 4] in sen_end or i[j + 3:j + 5] in sen_end or i[-2:len(
                i)] in sen_end:
            res.append(i[k + 2:j])
        #            i[j+1:j+3] in sen_end:
        else:
            words, postags = handler.cut_wds(i[j + 1:])
            if 'v' in postags and 'n' in postags:
                res.append(i[j + 1:])
            else:
                res.append(i[k + 2:j])

    elif '包括' in i and '的' in i:
        k = i.find('包括')
        j = i.find('的')
        if len(i[j + 1:]) <= 3:
            res.append(i[k + 2:j])
        elif i[j + 1:j + 3] in sen_end or i[j + 2:j + 4] in sen_end or i[j + 3:j + 5] in sen_end or i[-2:len(
                i)] in sen_end:
            res.append(i[k + 2:j])
        #            i[j+1:j+3] in sen_end:
        else:
            res.append(i[j + 1:])

    elif '阶段的' in i:
        k = i.find('阶段的')
        res.append(i[k + 3:])

    elif '中' in i:
        k = i.find('中')

        if '的' in i[k + 1]:
            j = i.index('的')
            words, postags = handler.cut_wds(i[j + 1:])

            if 'v' in postags:
                if postags.index('v') == 0 or postags.index('v') == 1:
                    wp = words[postags.index('v')]
                    lead = 1
            elif 'd' in postags:
                if postags.index('d') == 0 or postags.index('d') == 1:
                    wp = words[postags.index('d')]
                    lead = 1
            if len(i[j + 1:]) <= 3:
                if lead == 1:
                    res.append(i[k + 1:j] + wp)
                else:
                    res.append(i[k + 1:j])
            elif i[j + 1:j + 3] in sen_end or i[j + 2:j + 4] in sen_end or i[j + 3:j + 5] in sen_end or i[-2:len(
                    i)] in sen_end:
                if lead == 1:
                    res.append(i[k + 1:j] + wp)
                else:
                    res.append(i[k + 1:j])
            else:
                res.append(i[k + 1:])

        else:
            res.append(i[k + 1:])

    elif '一种' in i:  ###应用是动词，设备是vn
        k = i.find('一种')
        if '的' in i[k + 2:]:
            j = i.rfind('的')
            words, postags = handler.cut_wds(i[j + 1:])
            if 'v' in postags:
                if postags.index('v') == 0 or postags.index('v') == 1:
                    wp = words[postags.index('v')]
                    lead = 1
            elif 'd' in postags:
                if postags.index('d') == 0 or postags.index('d') == 1:
                    wp = words[postags.index('d')]
                    lead = 1

            if len(i[k + 1:]) <= 3:
                if lead == 1:
                    res.append(i[k + 2:j] + wp)
                else:
                    res.append(i[k + 2:j])
            elif i[j + 1:j + 3] in sen_end or i[j + 2:j + 4] in sen_end or i[j + 3:j + 5] in sen_end or i[-2:len(
                    i)] in sen_end:
                if lead == 1:
                    res.append(i[k + 2:j] + wp)
                else:
                    res.append(i[k + 2:j])
            #            i[j+1:j+3] in sen_end:
            elif i[k + 1:k + 4] == '仿真器':
                if lead == 1:
                    res.append(i[k + 2:j] + wp)
                else:
                    res.append(i[k + 2:j])
            else:
                res.append(i[k + 2:])

        elif '，' in i[k + 2:]:
            j = i.rfind('，')
            words, postags = handler.cut_wds(i[j + 1:])
            if 'v' in postags:
                if postags.index('v') == 0 or postags.index('v') == 1:
                    wp = words[postags.index('v')]
                    lead = 1
            elif 'd' in postags:
                if postags.index('d') == 0 or postags.index('d') == 1:
                    wp = words[postags.index('d')]
                    lead = 1

            if len(i[k + 1:]) <= 3:
                if lead == 1:
                    res.append(i[0:k] + wp)
                else:
                    res.append(i[0:k])
            elif i[k + 1:k + 3] in sen_end or i[k + 2:k + 4] in sen_end or i[k + 3:k + 5] in sen_end or i[-2:len(
                    i)] in sen_end:
                if lead == 1:
                    res.append(i[0:k] + wp)
                else:
                    res.append(i[0:k])
            #            i[j+1:j+3] in sen_end:
            elif i[k + 1:k + 4] == '仿真器':
                if lead == 1:
                    res.append(i[0:k] + wp)
                else:
                    res.append(i[0:k])
            else:
                res.append(i[k + 1:])

        else:
            res.append(i[k + 2:])

    elif '开发箱' in i:
        l = i.find('开发箱')
        res.append(i[0:l])
    elif '实验箱' in i:
        l = i.find('实验箱')
        res.append(i[0:l])
    elif '的' in i:  # many problem 本质进行的和方法的判断，可以设置第一个出现的名词为方法
        k = i.find('的')
        #        res.append(i[k+1:])

        words, postags = handler.cut_wds(i[k + 1:])
        #        if len(i)<=10:
        #            res.append(i)
        if 'v' in postags:
            if postags.index('v') == 0 or postags.index('v') == 1:
                wp = words[postags.index('v')]
                lead = 1
        elif 'd' in postags:
            if postags.index('d') == 0 or postags.index('d') == 1:
                wp = words[postags.index('d')]
                lead = 1

        if len(i[k + 1:]) <= 3:
            if lead == 1:
                res.append(i[0:k] + wp)
            else:
                res.append(i[0:k])
        elif i[k + 1:k + 3] in sen_end or i[k + 2:k + 4] in sen_end or i[k + 3:k + 5] in sen_end or i[-2:len(
                i)] in sen_end:
            if lead == 1:
                res.append(i[0:k] + wp)
            else:
                res.append(i[0:k])
        #            i[j+1:j+3] in sen_end:
        elif i[k + 1:k + 4] == '仿真器':
            if lead == 1:
                res.append(i[0:k] + wp)
            else:
                res.append(i[0:k])
        else:
            res.append(i[k + 1:])
    else:
        res.append(i)
    se.loc[m]['技术点'] = res

print(se.iloc[774]['技术点'])

################*******************************切分技术点****************************#######################
# 测试方法
se['切分后'] = None
for cc in range(len(se)):
    tech = se.loc[cc]['技术点'][0]
    if len(tech) > 10:
        print(cc)
        print(tech)

        if tech[len(tech) - 5:len(tech) - 3] in ['系统', '应用', '装置', '方法', '装置'] and tech[len(tech) - 2:len(tech)] in [
            '系统', '应用', '装置', '方法', '装置']:
            if tech[len(tech) - 6] == '的':
                tech = tech[0:len(tech) - 6]
            else:
                tech = tech[0:len(tech) - 5]

        #        print(se.loc[i]['技术点'][0]+'___'+np.str(i))
        if '的' in tech:
            k = tech.find('的')
            #        res.append(i[k+1:])
            words, postags = handler.cut_wds(tech[k + 1:])

            if 'v' in postags:
                if postags.index('v') == 0 or postags.index('v') == 1:
                    wp = words[postags.index('v')]
                    lead = 1

            if len(tech[k + 1:]) <= 3:
                if lead == 1:
                    res.append(tech[0:k] + wp)
                else:
                    res.append(tech[0:k])
            elif tech[k + 1:k + 3] in sen_end or tech[k + 2:k + 4] in sen_end or tech[k + 3:k + 5] in sen_end:
                if lead == 1:
                    res.append(tech[0:k] + wp)
                else:
                    res.append(tech[0:k])
            #            i[j+1:j+3] in sen_end:
            elif tech[k + 1:k + 4] == '仿真器':
                if lead == 1:
                    res.append(tech[0:k] + wp)
                else:
                    res.append(tech[0:k])
            else:
                res.append(tech[k + 1:])

        if len(tech) < 10:
            se.loc[cc]['切分后'] = tech
            continue
        words, postags = handler.cut_wds(tech)
        mi = 0
        while (mi < len(words)):
            if words[mi] in sen_end:
                del words[mi]
                del postags[mi]
                mi -= 1
            mi += 1
        if len(tech) < 10:
            se.loc[cc]['切分后'] = tech
            continue
        #        words, postags = handler.cut_wds('便携式通用数字逻辑设计和EDA综合实验板')
        postags = ['n' if i in ['l', 'n', 'z', 'eng', 'nz'] else i for i in postags]
        if 'v' not in postags and 'vn' not in postags:
            nu = []
            for i in range(len(postags)):
                if postags[i] == 'n' or postags[i] == 'd':
                    nu.append(words[i])
            if len(nu) > 5:
                nu = nu[0:5]
            se.loc[cc]['切分后'] = ''.join(nu)
            continue
        if 'v' not in postags and 'vn' in postags:
            postags = ['v' if i in ['vn'] else i for i in postags]
        own = []
        own_p = []
        act = []
        sub = []
        sub_p = []
        act_d = []

        for i in range(len(postags)):
            pi = postags[i]
            wi = words[i]
            ####获取主语
            if pi == 'n' and len(act) == 0:
                if len(own) <= 1:
                    own.append(wi)
                    own_p.append(pi)
                elif len(own) == 2:
                    if (own_p[1] == 'c' or own_p[1] == 'uj') and len(wi) > 1:
                        own.append(wi)
                        own_p.append(pi)

                elif len(own) == 3:
                    if (own_p[2] == 'uj' or own_p[2] == 'c') and len(wi) > 1:
                        own.append(wi)
                        own_p.append(pi)
                    elif (own_p[1] == 'uj' or own_p[1] == 'c') and len(wi) > 1:
                        own.append(wi)
                        own_p.append(pi)

            ###添加链接词
            elif (pi == 'uj' or pi == 'c') and len(own) >= 1 and len(act) == 0:
                if len(own) == 1:
                    own.append(wi)
                    own_p.append(pi)
                elif len(own) == 2 and own_p[1] == 'n':
                    own.append(wi)
                    own_p.append(pi)
            ######获取动词语
            elif (pi == 'v' or pi == 'vn') and len(sub) == 0:
                if len(act) == 0:
                    act.append(wi)
            #######获取宾语
            elif pi == 'n' and len(act) > 0:
                if len(sub) <= 1:
                    sub.append(wi)
                    sub_p.append(pi)
                elif len(sub) == 2:
                    if (sub_p[1] == 'c' or sub_p[1] == 'uj') and len(wi) > 1:
                        sub.append(wi)
                        sub_p.append(pi)
                    elif sub_p[1] == 'n':
                        sub.append(wi)
                        sub_p.append(pi)
                elif len(sub) == 3:
                    if (sub_p[2] == 'uj' or sub_p[2] == 'c') and len(wi) > 1:
                        sub.append(wi)
                        sub_p.append(pi)
                    elif (sub_p[1] == 'uj' or sub_p[1] == 'c') and len(wi) > 1:
                        sub.append(wi)
                        sub_p.append(pi)

            ###添加链接词
            elif (pi == 'uj' or pi == 'c') and len(sub) >= 1 and len(act) > 0:
                if len(sub) == 1:
                    sub.append(wi)
                    sub_p.append(pi)
                elif len(sub) == 2 and sub_p[1] == 'n':
                    sub.append(wi)
                    sub_p.append(pi)
            if len(act) > 0 and pi == 'd':
                act_d.append(wi)
            elif i < len(postags) - 1:
                if postags[i + 1] == 'v':
                    act_d.append(wi)

        if len(own) > 0:
            if own_p[-1] == 'uj' or own_p[-1] == 'c':
                del own[-1]
        if len(sub) > 0:
            if sub_p[-1] == 'uj' or sub_p[-1] == 'c':
                del sub[-1]
        #        print(act)
        if not own or not sub:
            se.loc[cc]['切分后'] = ''.join(own + act + act_d + sub)
        else:
            se.loc[cc]['切分后'] = ''.join(own + act + sub)
    else:
        se.loc[cc]['切分后'] = tech
opc_nu = []
opc_t = []
tcad_nu = []
tcad_t = []
good_rate_nu = []
good_rate_t = []
good_rate_name = []
good_rate_right = []
for sc in range(len(se['专利申请号'])):
    second_category = se.iloc[sc]['二级分类']
    if second_category == 'opc':
        opc_nu.append(se.iloc[sc]['专利申请号'])
        opc_t.append(se.iloc[sc]['切分后'])
        # opc_t.append(se.iloc[sc]['发明名称'])
    elif second_category == 'tcad':
        tcad_nu.append(se.iloc[sc]['专利申请号'])
        tcad_t.append(se.iloc[sc]['切分后'])
        # tcad_t.append(se.iloc[sc]['发明名称'])
    elif second_category == 'good_rate':
        good_rate_nu.append(se.iloc[sc]['专利申请号'])
        good_rate_t.append(se.iloc[sc]['切分后'])
        good_rate_name.append(se.iloc[sc]['发明名称'])
        good_rate_right.append(se.iloc[sc]['主权项'])
def save_txt(str_list:list,name):
    with open(name,'w',encoding='utf-8') as f:
        for i in str_list:
            f.write(i+'\n')
save_txt(opc_t, '..\data\opc.txt')
save_txt(tcad_t, '..\data\\tcad.txt')
save_txt(good_rate_t, '..\data\good_rate.txt')
save_txt(good_rate_right, '..\data\good_rate_right.txt')
se.to_excel('..\data\TP.xlsx')

LDA = lda.LDAClustering()
# ret,docres = LDA.lda('..\data\\tcad.txt', stopwords_path='..\data\stop_words2.txt', max_iter=100, n_components=5)
# ret,docres = LDA.lda('..\data\opc.txt', stopwords_path='..\data\stop_words2.txt', max_iter=100, n_components=8)
# ret,docres,tw = LDA.lda('..\data\good_rate.txt', stopwords_path='..\data\stop_words2.txt', max_iter=100, n_components=8)
ret,docres,tw = LDA.lda('..\data\good_rate_right.txt', stopwords_path='..\data\stop_words2.txt', max_iter=100, n_components=8)
print(ret[1])
print(tw[1])

label = []
number = []
topic_words = []
extract = []
names = []
right = []
clusters = pd.DataFrame(columns= ['主题标签','主题词','专利号','专利名称','技术词','主权项'])
for i,j in ret.items():
    # print(i,j)
    for k in j:
        label.append(i)
        topic_words.append(tw[i])
        number.append(good_rate_nu[k])
        extract.append(good_rate_t[k])
        names.append(good_rate_name[k])
        right.append(good_rate_right[k])
clusters['主题标签'] = label
clusters['主题词'] = topic_words
clusters['专利号'] = number
clusters['技术词'] = extract
clusters['专利名称'] = names
clusters['主权项'] = right
clusters.to_csv('..\data\goodratecluster.csv', index_label='id')