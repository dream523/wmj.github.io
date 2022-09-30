import pandas as pd
#data = pd.read_csv('/Users/wangmujie/Desktop/空间研究所实习/good_rate_202209271746.csv')
data = pd.read_csv('/Users/wangmujie/Desktop/空间研究所实习/tcad_202209271746.csv')
t_summary = data['abstract']
handler = ExtractEvent()
s = pd.DataFrame()
s['摘要'] = t_summary
s['功效'] = None

words = ['完善', '便于', '适用范围', '适用性', '明确', '参考性', '加快', '及时', '缩减', '拓展', '优选', '普适性', '准确', '不会', '提升', '精准', '缩短',
         '节约', '优点', '满足', '安全性高', '不变形', '体积较小', '体积小', '方便', '环保', '噪声低', '领先', '紧凑', '低成本', '有利', '改进', '成本低', '含量高',
         '不易松动', '低排放', '效率高', '转化高', '高纯度', '能耗低', '工艺简单', '有利于', '质量好', '污染小', '优异', '环保型', '舒适', '效益', '高性能', '更好',
         '较好', '高效稳定', '简化', '稳定', '减少', '解决', '需要', '可靠', '名副其实', '简单', '保证', '低廉', '准确性', '减小', '明显', '改善', '增加',
         '可靠性', '耐久性', '目标明确', '节能', '克服', '旨在克服', '提高', '合理', '降低', '节省', '高效', '改善', '性能', '成本', '效率', '安全', '无需',
         '抑制', '容易', '易于', '有效', '增加', '快捷', '快速', '显著', '适应', '旨在', '灵活', '增加', '利于', '快速', '促进', '规避', '显著', '丰富',
         '个大', '低廉', '繁殖率大', '处理量大', '范围大', '密度大', '大面积', '解决', '可避免', '无须', '消除', '迅速', '特性', '防止', '克服', '寿命', '适用性',
         '强', '避免', '推动', '分布均匀', '最好', '污染', '价值', '造价低', '损失', '更远', '免除', '只需', '修复', '有效', '较高', '简洁', '新颖', '均衡',
         '简便', '精确', '绿色化', '便于推广']
# 加速实现
# 针对 专利6
# 在...不变的情况下
# 集...于一体 专利10
# '便于' +words
###容易出现误识别的词语 需要
for k in range(len(s)):
    content = s.loc[k]['摘要']
    paras = handler.split_paras(content)
    for para in paras:
        long_sents = handler.split_long_sents(para)
    persons = []
    for long_sent in long_sents:
        short_sents = handler.split_short_sents(long_sent)
        persons += short_sents
    eff = []
    i = 0
    sign = 0
    while (i < len(persons)):
        if sign == 0 and '既可' in persons[i]:
            res = ''
            if '又可' in persons[i]:
                eff.append(persons[i])
            else:
                for j in range(i, len(persons)):
                    res += persons[j]
                    if '又可' in persons[j]:
                        eff.append(res)
                        i = j - 1
                        break
                    elif j == len(persons) - 1:
                        i -= 1
                        sign = 1

        elif sign == 0 and '与' in persons[i]:
            res = ''
            if '相比' in persons[i]:
                if persons[i].index('相比') < len(persons[i]) - 1:
                    eff.append(persons[i])
                else:
                    eff.append(persons[i] + persons[i + 1])
                    i += 1
            else:
                for j in range(i, len(persons)):
                    res += persons[j]
                    if '相比' in persons[j]:
                        if persons[j].index('相比') < len(persons[j]) - 1:
                            eff.append(res)
                            i = j
                            break
                        else:
                            eff.append(res + persons[j + 1])
                            i = j + 1
                            break
                    elif j == len(persons) - 1:
                        i -= 1
                        sign = 1

        elif sign == 0 and '解决' in persons[i]:
            res = ''
            if '问题' in persons[i]:
                eff.append(persons[i])
            else:
                for j in range(i, len(persons)):
                    res += persons[j]
                    if '问题' in persons[j]:
                        eff.append(res)
                        i = j
                        break
                    elif j == len(persons) - 1:
                        i -= 1
                        sign = 1

        elif sign == 0 and '不但' in persons[i]:
            res = ''
            if '而且' in persons[i]:
                eff.append(persons[i])
            else:
                for j in range(i, len(persons)):
                    res += persons[j]
                    if '而且' in persons[j]:
                        eff.append(res)
                        i = j
                        break
                    elif j == len(persons) - 1:
                        i -= 1
                        sign = 1

        elif sign == 0 and '集' in persons[i]:
            res = ''
            if '于一体' in persons[i]:
                eff.append(persons[i])
            else:
                for j in range(i, len(persons)):
                    res += persons[j]
                    if '于一体' in persons[j]:
                        eff.append(res)
                        i = j
                        break
                    elif j == len(persons) - 1:
                        i -= 1
                        sign = 1

        elif '实用' in persons[i] and '实用新型' not in persons[i]:
            sign = 0
            #        words, postags = handler.cut_wds(persons[i])
            eff.append(persons[i])
        elif '实现' in persons[i] and persons[i].find('实现') != len(persons[i]) - 2 and persons[i].find('实现') != len(
                persons[i]) - 4:  # 实现方法可能会误识别
            sign = 0
            eff.append(persons[i])
        else:
            sign = 0
            for j in words:
                if j in persons[i] and ('利用' not in persons[i] or '利用率' in persons[i]) and '包括' not in persons[
                    i] and not (persons[i][0].isdigit() and persons[i][1] == '）'):
                    eff.append(persons[i])
                    break
        i += 1
    s.loc[k]['功效'] = eff

##########################*************************功效点映射*************************##########################

accuracy = ['合格', '错误率', '明确', '科学', '错误', '失据', '失误', '偏差', '合理', '偏离', '误差', '遗漏', '易错', '完善', '过拟合', '完整', '全面',
            '失真', '精准', '高纯度', '准确', '精确', '精度', '对比度']
safe = '失败率 成功率 失效 无法 中断 损坏 损失 不良 危险 风险 绿色化 安全 安全性高 紧凑 污染小 噪声低 环保型 低排放 消除 污染 损失'.split(' ')
cost = '昂贵 节约 体积较小 体积小 环保 低成本 成本低 能耗低 低廉 节能 节省 成本 低廉 造价低'.split(' ')
reliable = '良率 良品 可维护性 抑制 异常 均衡 干扰 影响 误操作 修复 价值 处理量大 丰富 变形 含量高 不易松动 质量好 稳定 可靠 保证 名副其实 可靠性 耐久性 舒适 合理 性能 高性能 寿命 容错 实时'.split(
    ' ')
flexible = '复用 不需要 任意 统一 局限 集成 同步 方便 简便 新颖 简洁 只需 免除 无需 更远 推动 无须 范围大 大面积 灵活 适应 便于 适用范围 适用性 参考性 拓展 普适性 方便 工艺简单 简化 简单 容易 易于'.split(
    ' ')
efficiency = ['时间', '周期', '速率', '过填充', '费力', '费事', '多次', '重复', '麻烦', '繁重', '避免', '慢', '优化', '较高', '有效', '最好', '强', '迅速',
              '快速', '显著', '快速', '快捷', '有效', '效率', '高效', '优异', '明显', '分布均匀', '尺寸大', '个大', '密度大', '加快', '及时', '优选', '优点',
              '领先', '有利', '改进', '效率', '转化', '效益', '更快', '更好', '较好']  # 效率

s['label'] = None
label = []
for c in s['功效']:
    mid = []
    for i in c:
        res = ''
        for j in accuracy:
            if j in i:
                res = 1
                mid.append('准确性高')

        for j in safe:
            if j in i:
                res = 1
                mid.append('安全性强')

        for j in cost:
            if j in i:
                res = 1
                mid.append('成本低')

        for j in reliable:
            if j in i:
                res = 1
                mid.append('可靠性强')

        for j in flexible:
            if j in i:
                res = 1
                mid.append('灵活性高')
            elif '集' in i and '于一体' in i:
                res = 1
                mid.append('灵活性高')

        for j in efficiency:
            if j in i:
                res = 1
                mid.append('性能高')

        if not res and ('解决' in i or '获得' in i or '获取' in i or '实现' in i or '实用' in i):
            mid.append('灵活性高')
        if not res and ('提升' in i or '缩简' in i or '减少' in i or '增加' in i or '提高' in i or '降低' in i or '减小' in i):
            mid.append('性能高')
    if not mid:
        mid.append('灵活性高')
    label.append(','.join(list(set(mid))))

s['label'] = label