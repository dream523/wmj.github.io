###################*************************从字符中提取英文的技术*************************###################
def is_ustr(in_str):
    out_str=''
    for i in range(len(in_str)):
        if is_uchar(in_str[i]):
            out_str=out_str+in_str[i]
        else:
            out_str=out_str+' '
    return out_str
def is_uchar(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
            return False
    """判断一个unicode是否是数字"""
    if uchar >= u'\u0030' and uchar<=u'\u0039':
            return False
    """判断一个unicode是否是英文字母"""
    if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
            return True
    if uchar in ('-'):
            return False
    return False

###################*************************TCAD*************************###################
# math = ['贝叶斯','']
sk = pd.read_csv('/Users/wangmujie/Desktop/空间研究所实习/tcad_202209271746.csv')
se = sk[['patent_app_nu','abstract','patent_title']]
tech_title = []
for i in se['patent_title']:

    if '算法' in i or '函数' in i or '深度学习' in i:
        tech_title.append('算法仿真')
    elif '神经网络' in i or '建模' in i or '模型' in i or '人工智能' in i:
        tech_title.append('模型仿真')
    elif '工艺' in i or '设计' in i:
        tech_title.append('工艺设计仿真')
    elif '电路' in i or '电子' in i:
        tech_title.append('电子电路仿真')

    elif '自动化' in i or '自适应' in i:
        tech_title.append('自动化仿真')
    elif '控制' in i:
        tech_title.append('控制仿真')

    elif '验证' in i or '监测' in i or '检验' in i or '检测' in i:
        tech_title.append('验证与检测仿真')
    elif '监视' in i or '追踪' in i or '跟踪' in i or '监控' in i:
        tech_title.append('监视与追踪仿真')
    elif '定位' in i:
        tech_title.append('定位仿真')
    elif '测试' in i or '测验' in i:
        tech_title.append('仿真测试')
    elif '调整' in i or '调试' in i:
        tech_title.append('仿真调试')
    elif len(is_ustr(i).replace(' ', '')) > 0:
        tech_title.append(is_ustr(i).replace(' ', ''))
    elif '数据' in i or '数值' in i or '参数' in i:
        tech_title.append('数据仿真')
    elif '仿真' in i or '模拟' in i:
        if '装置' in i or '设备' in i or '系统' in i or '工具' in i:
            tech_title.append('仪器仿真')
        else:
            tech_title.append('方法仿真')
    elif '故障' in i or '缺陷' in i or '错误' in i:
        tech_title.append('缺陷与故障分析')
    elif '模组' in i or '模版' in i or '板块' in i or '板图' in i or '模板' in i or '膜版' in i:
        tech_title.append('模板仿真')


    elif '参数' in i or '数值' in i or '数据' in i:
        tech_title.append('参数与数据仿真')

    elif '芯片' in i or '半导体' in i or '单片机' in i or '硅' in i:
        tech_title.append('半导体与芯片仿真')
    elif '二极管' in i or '晶体管' in i:
        tech_title.append('二极管与晶体管仿真')
    elif '晶片' in i or '晶体' in i or '晶圆' in i:
        tech_title.append('晶体与晶片仿真')

    elif '图形' in i or '图案' in i:
        tech_title.append('图形图案仿真')

    elif '验证' in i or '检验' in i:
        tech_title.append('仿真验证')
    elif '界面' in i or '屏幕' in i:
        tech_title.append('屏幕界面仿真')
    elif '方法' in i or '策略' in i:
        tech_title.append('方法仿真')
    elif '系统' in i:
        tech_title.append('系统仿真')
    elif '装置' in i:
        tech_title.append('仪器仿真')
    elif '应用' in i:
        tech_title.append('方法策略')

    elif '终端' in i:
        tech_title.append('系统仿真')
    elif '平台' in i:
        tech_title.append('系统仿真')
    elif '仿真器' in i or '模拟器' in i:
        tech_title.append('仪器仿真')
    elif '反应堆' in i:
        tech_title.append('反应堆')
    elif '设备' in i or '器械' in i or '器件' in i or '器' in i or '仪' in i:
        tech_title.append('仪器仿真')
    #    elif '板' in i or '块' in i:
    #        tech_title.append('模板仿真')
    else:
        tech_title.append('')
#    else:
#        words,postags = handler.cut_wds(i)
#        if postags[-1] in ['l','n','eng','z','nz']:
#            tech_title.append('方法')
#        else:
#            tech_title.append('仪器')
se['new_label'] = tech_title

###################*************************OPC*************************###################
sk = pd.read_csv('/Users/wangmujie/Desktop/空间研究所实习/opc_202209271746.csv')
se = sk[['patent_app_nu','abstract','patent_title']]
tech_title = []
for i in se['patent_title']:

    if '识别' in i:
        if '装置' in i or '设备' in i or '系统' in i or '工具' in i:
            tech_title.append('识别装置')
        else:
            tech_title.append('识别方法')

    elif '控制' in i:
        if '装置' in i or '设备' in i or '系统' in i or '工具' in i:
            tech_title.append('控制装置')
        else:
            tech_title.append('控制方法')
    elif '监测' in i or '检验' in i or '检测' in i or '监控' in i or '跟踪' in i:
        if '装置' in i or '设备' in i or '系统' in i or '工具' in i:
            tech_title.append('监控与检测装置')
        else:
            tech_title.append('验证与检测方法')
    elif '定位' in i:
        if '装置' in i or '设备' in i or '系统' in i or '工具' in i:
            tech_title.append('定位装置')
        else:
            tech_title.append('定位方法')
    elif '验证' in i or '测试' in i or '测验' in i:
        if '装置' in i or '设备' in i or '系统' in i or '工具' in i:
            tech_title.append('测试装置')
        else:
            tech_title.append('测试方法')

    elif '算法' in i or '函数' in i or '深度学习' in i:
        tech_title.append('算法')
    elif '神经网络' in i or '模型' in i or '建模' in i:
        tech_title.append('建模')
    elif '成像' in i:
        tech_title.append('光学成像')

    elif '测试' in i:
        if '自动' in i:
            tech_title.append('自动化测试')
        else:
            tech_title.append('光学测试')
    elif '投影' in i or '投射' in i or '反射' in i:
        tech_title.append('投影投射技术')
    elif '电路' in i or '电子' in i:
        tech_title.append('电路和电子')
    elif '仿真' in i:
        tech_title.append('光学仿真')
    elif '雷达' in i:
        tech_title.append('雷达')
    elif '红外' in i:
        tech_title.append('红外线')
    elif '激光' in i:
        tech_title.append('激光')
    elif '曝光' in i:
        tech_title.append('曝光')

    elif '临近效应' in i or '邻近效应' in i or '邻近校正' in i or '邻近修正' in i:
        tech_title.append('光学邻近效应与校正')

    elif '掩膜' in i or '掩模' in i or '光罩' in i:
        tech_title.append('光罩技术')
    elif '光电' in i:
        tech_title.append('光电技术')
    elif '光刻' in i:
        if '设备' in i or '工具' in i or '光刻机' in i:
            tech_title.append('光刻设备')
        else:
            tech_title.append('光刻技术')
    elif '半导体' in i or '芯片' in i or '二极管' in i or '单片机' in i or '硅' in i:
        tech_title.append('芯片与半导体')
    elif '晶体' in i or '晶片' in i or '晶圆' in i:
        tech_title.append('晶体与晶片')
    elif '图形' in i or '图案' in i or '图像' in i:
        tech_title.append('图形图像')
    elif len(is_ustr(i).replace(' ', '')) > 0:
        tech_title.append(is_ustr(i).replace(' ', ''))
    elif '数值' in i or '参数' in i:
        tech_title.append('光学参数控制')
    elif '信号灯' in i or '交通灯' in i or '红绿灯' in i:
        tech_title.append('红绿灯')
    elif '检测' in i or '检验' in i:
        tech_title.append('光学检测')
    elif '计量' in i or '测量' in i or '计算' in i:
        tech_title.append('光学计算')
    elif '光源' in i or '光束' in i or '光阑' in i or '光线' in i or '射线' in i:
        tech_title.append('光线技术')
    elif '光' in i:
        tech_title.append('光学衍生技术')
    elif '工艺' in i:
        tech_title.append('光学工艺')
    elif '元件' in i or '组件' in i or '部件' in i or '单元' in i:
        tech_title.append('光学组件')
    elif '制作' in i or '制备' in i or '制造' in i or '设计' in i or '布置' in i:
        tech_title.append('光学设计与制作技术')
    elif '生成' in i or '形成' in i or '获取' in i or '输出' in i:
        tech_title.append('光学生成技术')
    elif '分类' in i or '分析' in i:
        tech_title.append('光学分析分类技术')
    elif '增加' in i or '减少' in i or '减小' in i or '缩减' in i or '提升' in i or '降低' in i or '提高' in i or '优化' in i or '改进' in i:
        tech_title.append('性能优化技术')
    elif '模组' in i or '模版' in i or '板块' in i or '板图' in i:
        tech_title.append('光学模版')
    elif '模块' in i:
        tech_title.append('光学模块')
    elif '显示' in i:
        tech_title.append('光学显示技术')

    elif '方法' in i:
        tech_title.append('光学方法')
    elif '系统' in i or '结构' in i:
        tech_title.append('光学系统')
    elif '装置' in i:
        tech_title.append('光学仪器')
    elif '应用' in i:
        tech_title.append('光学方法')
    elif '设备' in i:
        tech_title.append('光学仪器')
    elif '终端' in i:
        tech_title.append('光学系统')
    elif '平台' in i:
        tech_title.append('光学系统')
    elif '仿真器' in i or '模拟器' in i:
        tech_title.append('光学仿真')
    elif '检查器' in i or '处理器' in i or '器件' in i or '隔离器' in i:
        tech_title.append('光学仪器')
    elif '仪' in i or '器' in i:
        tech_title.append('光学仪器')
    else:
        words, postags = handler.cut_wds(i)
        if 'v' in postags:
            tech_title.append('光学方法')
        else:
            tech_title.append('光学仪器')
# del se['new_label']
se['new_label'] = tech_title

###################*************************良率控制*************************###################
tech_title = []
for i in se['patent_title']:

    if '识别' in i:
        if '装置' in i or '设备' in i or '系统' in i or '工具' in i:
            tech_title.append('识别装置')
        else:
            tech_title.append('识别方法')
    elif '电路' in i or '电子' in i:
        tech_title.append('电子与电路')
    elif '自动化' in i or '自适应' in i:
        if '装置' in i or '设备' in i or '系统' in i or '工具' in i:
            tech_title.append('自动化装置')
        else:
            tech_title.append('自动化方法')
    elif '控制' in i:
        if '装置' in i or '设备' in i or '系统' in i or '工具' in i:
            tech_title.append('控制装置')
        else:
            tech_title.append('控制方法')
    elif '监测' in i or '检验' in i or '检测' in i or '监控' in i:
        if '装置' in i or '设备' in i or '系统' in i or '工具' in i:
            tech_title.append('监控与检测装置')
        else:
            tech_title.append('验证与检测方法')
    elif '定位' in i:
        if '装置' in i or '设备' in i or '系统' in i or '工具' in i:
            tech_title.append('定位装置')
        else:
            tech_title.append('定位方法')
    elif '验证' in i or '测试' in i or '测验' in i:
        if '装置' in i or '设备' in i or '系统' in i or '工具' in i:
            tech_title.append('测试装置')
        else:
            tech_title.append('测试方法')
    elif '数据' in i or '数值' in i or '参数' in i:
        tech_title.append('数据控制')

    elif '仿真' in i or '模拟' in i:
        tech_title.append('仿真')
    elif len(is_ustr(i).replace(' ', '')) > 0:
        tech_title.append(is_ustr(i).replace(' ', ''))

    elif '故障' in i or '缺陷' in i:
        tech_title.append('缺陷与故障分析')
    elif '模组' in i or '模版' in i or '板块' in i or '板图' in i:
        tech_title.append('模版')

    elif '测试' in i or '测验' in i:
        tech_title.append('测试')

    elif '图形' in i or '图案' in i:
        tech_title.append('图形')

    elif '算法' in i or '函数' in i or '深度学习' in i:
        tech_title.append('算法')
    elif '神经网络' in i or '模型' in i or '建模' in i:
        tech_title.append('建模')
    elif '半导体' in i or '芯片' in i or '二极管' in i or '单片机' in i or '硅' in i:
        tech_title.append('芯片与半导体')
    elif '晶体' in i or '晶片' in i or '晶圆' in i:
        tech_title.append('晶体与晶片')
    elif '预测' in i:
        tech_title.append('预测方法')
    elif '数值' in i or '参数' in i:
        tech_title.append('参数控制')

    elif '计量' in i or '测量' in i or '计算' in i:
        tech_title.append('计算')
    elif '工艺' in i:
        tech_title.append('工艺')
    elif '光' in i or '掩膜' in i or '掩模' in i:
        tech_title.append('光学技术')
    elif '制作' in i or '制备' in i or '制造' in i or '设计' in i:
        tech_title.append('设计与制作技术')
    elif '生成' in i or '形成' in i or '获取' in i:
        tech_title.append('生成技术')
    elif '分类' in i or '分析' in i:
        tech_title.append('分析分类技术')
    elif '减少' in i or '减小' in i or '缩减' in i or '提升' in i or '降低' in i or '提高' in i or '优化' in i:
        tech_title.append('优化技术')

    elif '界面' in i or '屏幕' in i:
        tech_title.append('良率提高系统')
    elif '系统' in i or '结构' in i or '程序' in i:
        tech_title.append('良率提高系统')
    elif '装置' in i:
        tech_title.append('良率提高仪器')
    elif '应用' in i:
        tech_title.append('良率提高方法')
    elif '设备' in i:
        tech_title.append('良率提高仪器')
    elif '终端' in i:
        tech_title.append('良率提高系统')
    elif '平台' in i:
        tech_title.append('良率提高系统')
    elif '仿真器' in i or '模拟器' in i:
        tech_title.append('仿真仪器')
    elif '检查器' in i or '处理器' in i or '器件' in i or '隔离器' in i:
        tech_title.append('良率提高仪器')
    elif '方法' in i:
        tech_title.append('良率提高方法')
    else:
        words, postags = handler.cut_wds(i)
        if postags[-1] == 'n' or postags[-1] == 'l' or postags[-1] == 'z' or postags[-1] == 'eng' or postags[
            -1] == 'nz':
            tech_title.append('良率提高仪器')
        else:
            tech_title.append('良率提高方法')

# del se['new_label']
se['new_label'] = tech_title