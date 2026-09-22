/*filename csvfile "D:\博士\博二\邱正西\2016-2024年子宫肌瘤患者明细-医保类型.xlsx"  encoding='utf-8';*/
/*proc import file=csvfile*/
/*out=Zgjl.snzgjl_1*/
/*DBMS=xlsx replace;*/
/*delimiter=',';*/
/*getnames=yes;*/
/*RUN;*/

data work.demo;set zgjl.snzgjl_1;run;

/*筛选主诊断+5种手术方式*/
/*12086->7687*/
data demo1;set demo;
if index(ZYZD_ICD,'D25')>0 then output;
else delete;run;

/*7687->7413*/
/* 定义一个宏变量包含所有手术名称*/
%let surgery_list ="腹腔镜(单孔)经腹全子宫切除术","腹腔镜（单孔）子宫病损切除术","腹腔镜残余子宫颈切除术","腹腔镜辅助经阴道子宫扩大切除术",
"腹腔镜辅助阴道子宫切除术(LAVH)","腹腔镜经腹筋膜外子宫切除术","腹腔镜经腹全子宫切除术","腹腔镜经腹双子宫切除术",
"腹腔镜下阔韧带病损切除术","腹腔镜下子宫次全切除术","腹腔镜下子宫肌瘤剔除术","腹腔镜子宫病损切除术",
"腹腔镜子宫次全切除术","腹腔镜子宫肌瘤切除术","腹腔镜子宫肌瘤挖除术","腹腔镜子宫韧带病损切除术",
"腹式子宫肌瘤挖除术","高强度聚焦超声治疗","高强度聚焦超声治疗[HIFU]","宫腔镜子宫病损电切术","宫腔镜子宫病损切除术","宫腔镜子宫颈病损电切术","宫腔镜子宫颈病损切除术","经腹筋膜外全子宫切除术",
"经腹全子宫切除术","经腹子宫次全切除术","经腹子宫肌瘤挖除术","经阴道子宫病损切除术","经阴道子宫颈病损切除术","经阴道子宫切除术","阔韧带病损切除术","子宫病损切除术",
"子宫次全切除术","子宫肌瘤切除术","子宫颈肌瘤切除术","子宫右侧阔韧带肌瘤剔除术","子宫楔形切除术","子宫全切术，右侧卵巢切除术","子宫全切术","子宫全切除术+双侧输卵管切除术",
"子宫全切除术","子宫内膜射频消融术","子宫扩大切除术","子宫颈肿瘤切除术","子宫颈粘膜下肌瘤摘除术","子宫颈部分切除术","子宫颈病损切除术","子宫肌瘤挖除+双侧卵巢囊肿摘除术",
"子宫肌瘤切除术+左侧输卵管切除术+盆腔粘连松解术","子宫肌瘤海扶消融术","子宫动脉造影","子宫动脉栓塞术","子宫次全切术","子宫次广泛切除术","子宫部分切除术","子宫病损射频消融术",
"子宫病损的其他切除术或破坏术","阴式子宫全切除术+左侧卵巢囊肿切除术+双侧输卵管切除术+盆腔引流术+会阴修补术","阴式子宫切除术","阴道子宫切除术","新阴式非脱垂子宫经阴道子宫切除术","双子宫单侧切除术",
"全子宫切除术","其他和未特指子宫切除术","其他和未特指的腹式全子宫切除术","其他和未特指的腹部次全子宫切除术","开腹子宫全切术+右侧输卵管切除术+右侧卵巢囊肿剥除术","开腹子宫全切术+双侧输卵管切除术",
"开腹子宫全切+双侧输卵管切除术+左卵巢囊肿剥除术+肠粘连松解术","经阴道子宫颈切除术","经阴道子宫肌瘤摘除术","经阴道行子宫粘膜下肌瘤摘除术","经腹子宫全切术","经腹子宫全切+双侧输卵管切除","经腹子宫全部切除术",
"经腹子宫广泛切除术","经腹子宫次全切术","经腹子宫次切除术+左侧附件切除术","经腹下子宫肌瘤剥除术","经腹双子宫切除术","经腹全子宫切除术+肠粘连松解术+左侧附件包裹性积液切","经腹全子宫切除术(68.4)",
"经腹腔镜阴道联合子宫全切术+双侧输卵管切除术","经腹腔镜行子宫肌瘤挖除术","经腹扩大性全子宫切除术","经腹筋膜外子宫全切术+双侧附件切除术+盆腔分粘术","筋膜外全子宫切除术","筋膜内子宫切除术[CISH手术]",
"宫腔镜子宫内膜切除术","宫腔镜子宫内膜病损切除术","宫腔镜子宫颈切除术","宫腔镜下子宫粘膜下肌瘤切除术","宫腔镜下子宫内膜赘生物电切术","宫腔镜下子宫内膜病损切除术","宫腔镜下子宫肌瘤挖除术","宫腔镜下子宫肌瘤切除术",
"宫腔镜下子宫病损射频消融术","宫腔镜下子宫病损切除术","宫腔镜下子宫病损电切术","宫腔镜下粘膜下子宫肌瘤切除术","宫腔镜下检查术及宫内病灶电切术","宫腔镜检查术+宫腔镜下黏膜下子宫肌瘤切除术","宫颈周围子宫去神经术","宫颈肌瘤剔除术",
"腹子宫次全切除术","腹式全子宫切除术","腹腔镜子宫修补术","腹腔镜子宫颈上子宫切除术[LSH]","腹腔镜子宫肌瘤剔除+右卵巢囊肿剥除+右输卵管部分切除","腹腔镜子宫病损电凝术","腹腔镜下子宫韧带肿瘤切除术","腹腔镜下子宫全切术",
"腹腔镜下子宫全切除术","腹腔镜下子宫扩大切除术","腹腔镜下子宫颈病损切除术","腹腔镜下子宫肌瘤挖除术+左侧卵巢囊肿剥除术+右侧输卵管系","腹腔镜下子宫肌瘤挖除术","腹腔镜下子宫肌瘤切除术","腹腔镜下子宫肌瘤剥除术","腹腔镜下子宫广泛性切除术",
"腹腔镜下子宫断蒂止血术","腹腔镜下子宫次全切术","腹腔镜下子宫病损切除术","腹腔镜下子宫病损电凝术","腹腔镜下全子宫切除术","腹腔镜下经腹子宫全切除术","腹腔镜下筋膜外子宫切除术","腹腔镜下次全子宫切除术",
"腹腔镜经腹子宫扩大切除术","腹腔镜辅助下阴式子宫切除，双侧输卵管切除术","腹腔镜辅助经阴道子宫广泛性切除术","腹腔镜辅助经阴道子宫次全切除术","腹腔镜辅助经阴道全子宫切除术[LAVH手术]","腹腔镜辅助经阴道筋膜内子宫切除术",
"腹腔镜残角子宫切除术","腹腔镜(宫腔镜)下子宫肌瘤挖除术","腹腔镜(宫腔镜)下子宫次全切术","单孔腹腔镜子宫病损切除术","标准子宫筋膜内子宫切除术";
data demo1;
     set demo1;
	 if SSJCZMC1 in (&surgery_list) then output;
	 else if SSJCZMC2 in (&surgery_list) then output;
     else if SSJCZMC3 in (&surgery_list) then output;
	 else if SSJCZMC4 in (&surgery_list) then output;
	 else if SSJCZMC5 in (&surgery_list) then output;
	 run;

/*添加标签*/
data demo1;set demo1;
    label YLJGID='机构ID'
CSRQ='出生日期'
JJLX='经济类型'
MZ= '民族'
SFZH= '身份证号'
ZY= '职业'
ZYCS='住院次数'
HY= '婚姻'
XZZ_XZQH= '现住址行政区划'
RYSJ= '入院时间'
CYSJ= '出院时间'
ZYZD= '主要诊断'
JBDM= '疾病编码'
QTZD1= '其他诊断1'
JBDM1= '疾病编码1'
QTZD2= '其他诊断2'
JBDM2= '疾病编码2'
QTZD3= '其他诊断3'
JBDM3= '疾病编码3'
QTZD4= '其他诊断4'
JBDM4= '疾病编码4'
QTZD5= '其他诊断5'
JBDM5= '疾病编码5'
SSJCZBM1= '手术及操作编码'
SSJCZMC1= '手术及操作名称'
SSJCZBM2= '手术及操作编码'
SSJCZMC2= '手术及操作名称'
SSJCZBM3= '手术及操作编码'
SSJCZMC3= '手术及操作名称'
SSJCZBM4= '手术及操作编码'
SSJCZMC4= '手术及操作名称'
SSJCZBM5= '手术及操作编码'
SSJCZMC5= '手术及操作名称'
LYFS= '离院方式'
ZFY= '住院费用(元)：总费用'
YLFUF= '综合医疗服务类：(1)一般医疗服务费'
ZLCZF= '一般治疗操作费'
HLF= '护理费'
QTFY= '其他费用'
BLZDF= '诊断类：(5)病理诊断费'
SYSZDF= '实验室诊断费'
YXXZDF= '影像学诊断费'
LCZDXMF= '临床诊断项目费'
FSSZLXMF= '治疗类(9)非手术治疗项目费'
WLZLF= '临床物理治疗费'
SSZLF= '手术治疗费'
MAF= '麻醉费'
SSF= '手术费'
KFF= '康复类(11)康复费'
ZYZLF= '中医类:(12)中医治疗费'
ZYL_ZYZD= '中医类(中医和名族医医疗服务)（12）中医诊断'
ZYWZ= '中医外治'
ZYGS= '中医骨伤'
ZCYJF= '针刺与灸法'
ZYTNZL= '中医推拿治疗'
ZYGCZL= '中医肛肠治疗'
ZYTSZL= '中医特殊治疗'
ZYQT= '中医其他'
ZYTSTPJG= '中医特殊调配加工'
BZSS= '辨证施膳'
XYF= '西药类:(13)西药费'
KJYWF= '抗菌药物费'
ZCYF= '中药类(16)中成药费'
ZYZJF= '医疗机构中药制剂费'
ZCYF1= '中草药费'
XF= '血液和血液制品类:(16)血费'
BDBLZPF= '白蛋白类制品费'
QDBLZPF= '球蛋白类制品费'
NXYZLZPF= '凝血因子类制品费'
XBYZLZPF= '细胞因子类制品费'
HCYYCLF= '耗材类(23)检查用一次性医用材料费'
YYCLF= '治疗用一次性医用材料费'
YCXYYCLF= '手术用一次性医用材料费'
QTF= '其他类(26)其他费'
ZYH='住院号'
YBLX='医保类型';
run;

/*转换数据类型和格式*/
/*proc contents data=demo1;run;*/
data demo1;set demo1;
birthday = input(CSRQ, anydtdte20.);
date1=input(rysj,anydtdte20.);
date2=input(cysj,anydtdte20.);
format birthday yymmdd10.;
format date1 yymmdd10.;
format date2 yymmdd10.;
ZYTS=date2-date1;
age=(date1-birthday)/365.25;
year= substr(CYSJ, 1, 4);
year1= substr(CYSJ, 1, 7);
ZFY0=input(ZFY,10.);
run;

%let hifu_9="高强度聚焦超声治疗","高强度聚焦超声治疗[HIFU]","子宫肌瘤海扶消融术","HIFU超声消融","子宫肌瘤超声消融术","超声消融治疗","子宫肌瘤超声消融治疗","海扶超声消融治疗";
%let ssfs_1="宫腔镜子宫病损电切术","宫腔镜子宫病损切除术","宫腔镜子宫颈病损电切术","宫腔镜子宫颈病损切除术","宫腔镜子宫内膜切除术","宫腔镜子宫内膜病损切除术","宫腔镜子宫颈切除术","宫腔镜下子宫粘膜下肌瘤切除术","宫腔镜下子宫内膜赘生物电切术","宫腔镜下子宫内膜病损切除术","宫腔镜下子宫肌瘤挖除术","宫腔镜下子宫肌瘤切除术","宫腔镜下子宫病损切除术","宫腔镜下子宫病损电切术","宫腔镜下粘膜下子宫肌瘤切除术","宫腔镜下检查术及宫内病灶电切术","宫腔镜检查术+宫腔镜下黏膜下子宫肌瘤切除术";
%let ssfs_2="腹腔镜子宫肌瘤剥除术","腹腔镜（单孔）子宫病损切除术","腹腔镜下阔韧带病损切除术","腹腔镜下子宫肌瘤剔除术","腹腔镜子宫病损切除术","腹腔镜子宫肌瘤切除术","腹腔镜子宫肌瘤挖除术","腹腔镜子宫韧带病损切除术","经腹腔镜行子宫肌瘤挖除术","腹腔镜子宫修补术","腹腔镜子宫肌瘤剔除+右卵巢囊肿剥除+右输卵管部分切除","腹腔镜子宫病损电凝术","腹腔镜下子宫韧带肿瘤切除术","腹腔镜下子宫颈病损切除术","腹腔镜下子宫肌瘤挖除术+左侧卵巢囊肿剥除术+右侧输卵管系","腹腔镜下子宫肌瘤挖除术","腹腔镜下子宫肌瘤切除术","腹腔镜下子宫肌瘤剥除术","腹腔镜下子宫断蒂止血术","腹腔镜下子宫病损切除术","腹腔镜下子宫病损电凝术","腹腔镜残角子宫切除术","腹腔镜(宫腔镜)下子宫肌瘤挖除术","腹腔镜(宫腔镜)下子宫次全切术","单孔腹腔镜子宫病损切除术";
%let ssfs_3="经腹子宫肌瘤剥除术","腹式子宫肌瘤挖除术","经腹子宫肌瘤挖除术","阔韧带病损切除术","子宫病损切除术","子宫肌瘤切除术","子宫颈肌瘤切除术","子宫右侧阔韧带肌瘤剔除术","子宫楔形切除术","子宫肌瘤挖除+双侧卵巢囊肿摘除术","子宫肌瘤切除术+左侧输卵管切除术+盆腔粘连松解术","子宫病损的其他切除术或破坏术","经腹下子宫肌瘤剥除术";
%let ssfs_4="经阴道子宫病损切除术","经阴道子宫切除术","阴式子宫全切除术+左侧卵巢囊肿切除术+双侧输卵管切除术+盆腔引流术+会阴修补术","阴式子宫切除术","阴道子宫切除术","新阴式非脱垂子宫经阴道子宫切除术","经阴道子宫颈病损切除术","子宫颈肿瘤切除术","子宫颈粘膜下肌瘤摘除术","子宫颈部分切除术","子宫颈病损切除术","经阴道子宫肌瘤摘除术","经阴道行子宫粘膜下肌瘤摘除术","宫颈肌瘤剔除术";
%let ssfs_5="腹腔镜(单孔)经腹全子宫切除术","腹腔镜辅助经阴道子宫扩大切除术","腹腔镜经腹筋膜外子宫切除术","腹腔镜经腹全子宫切除术","腹腔镜经腹双子宫切除术","腹腔镜下子宫次全切除术","腹腔镜子宫次全切除术","腹腔镜子宫颈上子宫切除术[LSH]","腹腔镜下子宫全切术","腹腔镜下子宫全切除术","腹腔镜下子宫扩大切除术","腹腔镜下子宫广泛性切除术","腹腔镜下子宫次全切术","腹腔镜下全子宫切除术","腹腔镜下经腹子宫全切除术","腹腔镜下筋膜外子宫切除术","腹腔镜下次全子宫切除术","腹腔镜经腹子宫扩大切除术","标准子宫筋膜内子宫切除术","筋膜内子宫切除术[CISH手术]";
%let ssfs_7="经腹次全子宫切除术","经腹子宫全切除术","经腹筋膜外全子宫切除术","经腹全子宫切除术","经腹子宫次全切除术","子宫次全切除术","子宫全切术，右侧卵巢切除术","子宫全切术","子宫全切除术+双侧输卵管切除术","子宫全切除术","子宫扩大切除术","子宫次全切术","子宫次广泛切除术","子宫部分切除术","双子宫单侧切除术","全子宫切除术","其他和未特指子宫切除术","其他和未特指的腹式全子宫切除术","其他和未特指的腹部次全子宫切除术","开腹子宫全切术+右侧输卵管切除术+右侧卵巢囊肿剥除术","开腹子宫全切术+双侧输卵管切除术","开腹子宫全切+双侧输卵管切除术+左卵巢囊肿剥除术+肠粘连松解术","经腹子宫全切术","经腹子宫全切+双侧输卵管切除","经腹子宫全部切除术","经腹子宫广泛切除术","经腹子宫次全切术","经腹子宫次切除术+左侧附件切除术","经腹双子宫切除术","经腹全子宫切除术+肠粘连松解术+左侧附件包裹性积液切","经腹全子宫切除术(68.4)","经腹扩大性全子宫切除术","经腹筋膜外子宫全切术+双侧附件切除术+盆腔分粘术","筋膜外全子宫切除术","腹子宫次全切除术","腹式全子宫切除术";
%let ssfs_8="腹腔镜辅助阴道子宫切除术(LAVH)","经腹腔镜阴道联合子宫全切术+双侧输卵管切除术","腹腔镜辅助下阴式子宫切除，双侧输卵管切除术","腹腔镜辅助经阴道子宫广泛性切除术","腹腔镜辅助经阴道子宫次全切除术","腹腔镜辅助经阴道全子宫切除术[LAVH手术]","腹腔镜辅助经阴道筋膜内子宫切除术";
/*%let ssfs_10=" ","-","--","诊断性刮宫术","诊刮术","宫腔镜诊断性刮宫术","诊断性刮宫";*/
/*******************************变量分类 变量清理*******************************************************/
data demo1;
    set demo1;
/*HIFU=9*/
    if SSJCZMC1 in (&hifu_9) or
       SSJCZMC2 in (&hifu_9) or
       SSJCZMC3 in (&hifu_9) or
       SSJCZMC4 in (&hifu_9) or
       SSJCZMC5 in (&hifu_9)
       then ssfs = 9;
/*宫腔镜剔肌瘤*/
    else if SSJCZMC1 in (&ssfs_1) or
       SSJCZMC2 in (&ssfs_1) or
       SSJCZMC3 in (&ssfs_1) or
       SSJCZMC4 in (&ssfs_1) or
	   SSJCZMC5 in (&ssfs_1) 
       then ssfs =1;
/*腹腔镜剔肌瘤*/
    else if SSJCZMC1 in (&ssfs_2) or
       SSJCZMC2 in (&ssfs_2) or
       SSJCZMC3 in (&ssfs_2) or
       SSJCZMC4 in (&ssfs_2) or
       SSJCZMC5 in (&ssfs_2)
       then ssfs = 2;
/*开腹剔肌瘤*/
   else if SSJCZMC1 in (&ssfs_3) or
       SSJCZMC2 in (&ssfs_3) or
       SSJCZMC3 in (&ssfs_3) or
       SSJCZMC4 in (&ssfs_3) or
       SSJCZMC5 in (&ssfs_3)
       then ssfs = 3;
/*阴式剔肌瘤*/
    else if SSJCZMC1 in (&ssfs_4) or
       SSJCZMC2 in (&ssfs_4) or
       SSJCZMC3 in (&ssfs_4) or
       SSJCZMC4 in (&ssfs_4) or
       SSJCZMC5 in (&ssfs_4)
       then ssfs = 4;
/*腹腔镜切子宫*/
    else if SSJCZMC1 in (&ssfs_5) or
       SSJCZMC2 in (&ssfs_5) or
       SSJCZMC3 in (&ssfs_5) or
       SSJCZMC4 in (&ssfs_5) or
       SSJCZMC5 in (&ssfs_5)
       then ssfs = 5;
/*腹腔镜残余子宫颈切除*/
    else if SSJCZMC1 in ("腹腔镜残余子宫颈切除术") or
       SSJCZMC2 in ("腹腔镜残余子宫颈切除术") or
       SSJCZMC3 in ("腹腔镜残余子宫颈切除术") or
       SSJCZMC4 in ("腹腔镜残余子宫颈切除术") or
       SSJCZMC5 in ("腹腔镜残余子宫颈切除术")
       then ssfs = 6;
/*开腹切子宫*/
    else if SSJCZMC1 in (&ssfs_7) or
       SSJCZMC2 in (&ssfs_7) or
       SSJCZMC3 in (&ssfs_7) or
       SSJCZMC4 in (&ssfs_7) or
       SSJCZMC5 in (&ssfs_7)
       then ssfs = 7;
/*腹腔镜辅助阴式子宫切除(LAVH)*/
    else if SSJCZMC1 in (&ssfs_8) or
       SSJCZMC2 in (&ssfs_8) or
       SSJCZMC3 in (&ssfs_8) or
       SSJCZMC4 in (&ssfs_8) or
       SSJCZMC5 in (&ssfs_8)
       then ssfs = 8;
/*子宫内膜/病损射频消融术*/
    else if SSJCZMC1 in ("子宫内膜射频消融术","子宫病损射频消融术","宫腔镜下子宫病损射频消融术") or
       SSJCZMC2 in ("子宫内膜射频消融术","子宫病损射频消融术","宫腔镜下子宫病损射频消融术") or
       SSJCZMC3 in ("子宫内膜射频消融术","子宫病损射频消融术","宫腔镜下子宫病损射频消融术") or
       SSJCZMC4 in ("子宫内膜射频消融术","子宫病损射频消融术","宫腔镜下子宫病损射频消融术") or
       SSJCZMC5 in ("子宫内膜射频消融术","子宫病损射频消融术","宫腔镜下子宫病损射频消融术")
       then ssfs = 10;
/*子宫动脉栓塞*/
    else if SSJCZMC1 in ("子宫动脉造影","子宫动脉栓塞术","子宫动脉栓塞[UAE]不伴弹簧圈","子宫动脉造影及栓塞术") or
       SSJCZMC2 in ("子宫动脉造影","子宫动脉栓塞术","子宫动脉栓塞[UAE]不伴弹簧圈","子宫动脉造影及栓塞术") or
       SSJCZMC3 in ("子宫动脉造影","子宫动脉栓塞术","子宫动脉栓塞[UAE]不伴弹簧圈","子宫动脉造影及栓塞术") or
       SSJCZMC4 in ("子宫动脉造影","子宫动脉栓塞术","子宫动脉栓塞[UAE]不伴弹簧圈","子宫动脉造影及栓塞术") or
       SSJCZMC5 in ("子宫动脉造影","子宫动脉栓塞术","子宫动脉栓塞[UAE]不伴弹簧圈","子宫动脉造影及栓塞术")
       then ssfs = 11;
/*宫颈周围子宫去神经术*/
    else if SSJCZMC1 in ("宫颈周围子宫去神经术") or
       SSJCZMC2 in ("宫颈周围子宫去神经术") or
       SSJCZMC3 in ("宫颈周围子宫去神经术") or
       SSJCZMC4 in ("宫颈周围子宫去神经术") or
       SSJCZMC5 in ("宫颈周围子宫去神经术")
       then ssfs = 12;
/*经阴道子宫颈切除术*/
	else if SSJCZMC1 in ("经阴道子宫颈切除术") or
       SSJCZMC2 in ("经阴道子宫颈切除术") or
       SSJCZMC3 in ("经阴道子宫颈切除术") or
       SSJCZMC4 in ("经阴道子宫颈切除术") or
       SSJCZMC5 in ("经阴道子宫颈切除术")
       then ssfs =13;
/*无治疗或仅操作（仅操作--诊断性刮宫术）*/
/*	else if SSJCZMC1 in (&ssfs_10) and*/
/*       SSJCZMC2 in (&ssfs_10) and*/
/*       SSJCZMC3 in (&ssfs_10) and*/
/*       SSJCZMC4 in (&ssfs_10) and*/
/*       SSJCZMC5 in (&ssfs_10)*/
/*       then ssfs =14;*/
/*	else ssfs=15;*/
   if age<18 then yyq=0;
   if 18=<age<45 then yyq=1;
   if 45=<age then yyq=2;
/*年龄分层*/
   if age<45 then age1=0;
   if age>=45 then age1=1;
   if age<30 then age2=0;
   if age>=30 then age2=1;
   if age<35 then age3=0;
   if age>=35 then age3=1;
/*年龄age5*/
   if age<30 then age4=0;
   if 30<=age<45 then age4=1;
   if age>=45 then age4=2;
   if age<35 then age5=0;
   if 35<=age<45 then age5=1;
   if age>=45 then age5=2;
/*ssz手术组4类*/
if ssfs=9 then ssz=0;*FUAS;
if ssfs=1 then ssz=2;
if ssfs=2 then ssz=2;
if ssfs=3 then ssz=2;
if ssfs=4 then ssz=2;
if ssfs=5 then ssz=1;
if ssfs=6 then ssz=3;
if ssfs=7 then ssz=1;
if ssfs=8 then ssz=1;
if ssfs=10 then ssz=3;
if ssfs=11 then ssz=3;
if ssfs=12 then ssz=3;
if ssfs=13 then ssz=3;
/*fuas和other*/
if ssfs=9 then fuas=1;
else fuas=0;
/*sszx手术组细类*/
if ssfs=9 then sszx=9;
if ssfs=1 then sszx=1;
if ssfs=2 then sszx=2;
if ssfs=3 then sszx=3;
if ssfs=4 then sszx=4;
if ssfs=5 then sszx=5;
if ssfs=6 then sszx=0;
if ssfs=7 then sszx=7;
/*LAVH合并腹腔镜切子宫*/
if ssfs=8 then sszx=5;
if ssfs=10 then sszx=10;
if ssfs=11 then sszx=11;
if ssfs=12 then sszx=0;
if ssfs=13 then sszx=0;
/*ZYTS分类*/
if 0=<ZYTS=<3 then ZYTS1=1;
if 3<ZYTS<7 then ZYTS1=2;
if 7=<ZYTS then ZYTS1=3;
/*HY婚姻*/
if HY="已婚" then HY1=1;
else HY1=0;
if sszx in (3, 7) then tr=0;
    else if sszx in (1, 2, 5, 4) then tr=1;  
    else tr=2;
/*切子宫与保子宫*/
if sszx in (5,7) then qzg=1;
	else qzg=0;
if sszx=0 then delete;
if YBLX="城镇职工基本医疗保险" then yblx1=0;
	else if YBLX="城镇居民基本医疗保险" then yblx1=1;
	else if YBLX="新型农村合作医疗" then yblx1=2;
	else yblx1=3;
/*合并 新型农村合作医疗 and others yblx2=1*/
if yblx1=2 then yblx2=1;
else if yblx1=3 then yblx2=1; 
else yblx2=0;
run; 

data demo1;set demo1;
label ZYTS='住院时长'
ssfs='手术方式'
ssz='手术组'
age='年龄'
HY1='婚姻'
sszx='Treatment Pattern'
ZYTS1='住院时长分类'
yblx1='医保类型'
;
run;

/* 创建一个格式，为ssfs的不同值设置标签 */
proc format;
   value ssfsfmt
      1 = '宫腔镜治疗'
      2 = '腹腔镜剥除'
      3 = '开腹肌瘤剥除'
      4 = '阴式肌瘤剥除'
      5 = '腹腔镜子宫全切'
      6 = '腹腔镜残余子宫颈切除'
      7 = '开腹子宫全切'
      8 = '腹腔镜辅助阴式子宫切除(LAVH)'
      9 = 'FUAS'
	  10='子宫内膜/病损射频消融术'
	  11='子宫动脉栓塞'
	  12='宫颈周围子宫去神经术'
	  13='经阴道宫颈切除'
	  14='无治疗';
value sszxfmt
      1 = 'HM'
      2 = 'LM'
      3 = 'AM'
      4 = 'VM'
      5 = 'LH'
      7 = 'OH'
      9 = 'FUAS'
	  10='RFA'
	  11='UAE';
value sszfmt
      0 = 'FUAS'
      1 = '切子宫'
      2 = '剔肌瘤'
      3 = '其他手术';
value fuasfmt
      1 = 'FUAS'
      0 = 'other';
value HY1fmt  0 = '其他' 1 = '已婚';
value age5fmt 0="age<35" 1="35≤age＜45" 2="45≤age";
value qzgfmt 0="保子宫" 1="切子宫";
value trfmt  0='open'  1='minimally' 2='image-guided';
value yblx1fmt  0='UEBMI'  1='URBMI' 2='NVCMI' 3='Others';
run;
data demo1;
   set demo1;
   format ssfs ssfsfmt.;
   format sszx sszxfmt.;
   format ssz sszfmt.;
   format HY1 HY1fmt.;
   format age5 age5fmt.;
   format qzg qzgfmt.;
   format fuas fuasfmt.;
   format tr trfmt.;
   format yblx1 yblx1fmt.;
run;
/********************DRG-E-CHAID算法数据集*/
data demo_d;
set demo1;keep age sszx zyts ZFY0 tr;run;
/******************************************/
data demo1;set demo1;
	if age=" " then delete;
	if ZFY0=" " then delete;
    if ZYTS=" " then delete;
	if age<15 then age=15;
run;

/*Table 1:Patient characteristics by uterine removal or preservation from 2016 to 2024*/
proc freq data=demo1;
table tr*sszx/fisher;run; 

proc freq data=demo1;
table tr*age5;run;

proc freq data=demo1;
table HY1*tr;run;

proc freq data=demo1 ;
table yblx1*tr;run;

proc freq data=demo1;
table HY1*tr;run;

proc means data=demo1 ;var ZYTS;class tr;run;
proc means data=demo1 ;var ZFY;class tr;run;

proc means data=demo1 mean std maxdec=2;
    where yblx1=1;
    var ZYTS;
    class year tr;
run;

/*最终7413*/
/************************************数据清洗结束***********************************************/
/*创建颜色表myattrmap*/
/*myid  其他  CXFF8884   CXFF8884*/
/*myid  LAVH  CXC82423   CXC82423*/
data myattrmap;
length value $ 20 linecolor $ 20 markercolor $ 20;
input ID $ value $ linecolor $ markercolor $;
datalines;
myid  LH  #42B540  #42B540
myid  OH  #ED0000  #ED0000
myid  LM  #5C96B1  #5C96B1
myid  HM  #57C0DB  #57C0DB
myid  AM  #3A6D9C #3A6D9C
myid  FUAS #CB9185 #CB9185
myid  VM  #A5DEEE #A5DEEE
myid  RFA  #E0E4FA  #E0E4FA
myid  UAE  #DEF2F1  #DEF2F1
;
run;
/*创建颜色映射表myattrmap1*/
data myattrmap1;
length value $ 20 linecolor $ 20 fillcolor $ 20;
input ID $ value $ linecolor $ fillcolor $;
datalines;
myid  LH  #42B540  #42B540
myid  OH  #ED0000  #ED0000
myid  LM  #5C96B1  #5C96B1
myid  HM  #57C0DB  #57C0DB
myid  AM  #3A6D9C #3A6D9C
myid  FUAS #CB9185 #CB9185
myid  VM  #A5DEEE #A5DEEE
myid  RFA  #E0E4FA  #E0E4FA
myid  UAE  #DEF2F1  #DEF2F1
;
run;
/**********************************************************/

/*Fig 2 Temporal trend of UFs treatments from 2016-2024*/
/************总体描述age5**************************/
%macro loop_years_Frequency;
%do year=2016 %to 2024;
proc surveyfreq data=demo1;
    where year="&year.";
    tables age5/ cl;
    ods output OneWay=freqout;
run;
data OneWay&year.;
     set freqout;
	 if age5=" " then delete;
     keep age5 Frequency Percent;
run;
%end;
%mend;
%loop_years_Frequency;
data all_oneway;
set oneway2016-oneway2024 indsname=dsname;  /* 获取数据集名称 */
length dsname_part $32;                    /* 存储数据集名部分 */
dsname_part = scan(dsname, -1, '.');       /* 提取数据集名（去掉库名） */
year = input(substr(dsname_part, 7), 4.);  /* 提取年份并转换为数值 */
keep age5 Frequency year Percent;                    /* 保留所需变量 */
rename age5=Group;
run;
/* 创建属性映射数据集，定义组颜色 */
data myattrmap3;
    length id $ 10 value $ 20 linecolor $ 20 markercolor $ 20;
    input id $ value $ linecolor $ markercolor $;
    datalines;
myid age<35 #4AC7A1 #4AC7A1
myid 35≤age＜45 #5C96B1 #5C96B1
myid 45≤age #5B7F75 #5B7F75
;
run;

/* 创建自定义y轴格式 */
proc format;
    picture kformat
        low - 0 = '0' (noedit)
        1000 - 10000 = 000k (prefix='' mult=0.001)
        10000 - high = 000k (prefix='' mult=0.001)
    ;
run;

ods listing gpath="D:\博士\博二\邱正西\Fig" image_dpi=300;
ods graphics / imagename="fig2_age5-" outputfmt=png width=8in height=6in border=off;

proc sgplot data=all_oneway dattrmap=myattrmap3 noautolegend;
    series x=year y=Frequency / 
        group=Group attrid=myid
        lineattrs=(pattern=solid thickness=2) 
        markers markerattrs=(size=12 symbol=CIRCLEFILLED) 
        datalabel=Frequency;
    keylegend "myAttrs" / location=inside position=topleft down=2;
    title " ";
    xaxis label="Year" values=(2016 to 2024 by 1) labelattrs=(size=16) valueattrs=(size=16);
    yaxis label="Number of UFs treatment" 
          values=(0 to 700 by 100)
          labelattrs=(size=16) 
          valueattrs=(size=16);
    keylegend / location=inside position=topleft down=3;
run;

ods graphics / reset;
ods listing close;

proc freq data=demo1;table sszx;run;
/*这里删除RFA和UAE数据7413->7407*/
data demo2;set demo1;
if sszx=10 or sszx=11 THEN delete;
run;

/*Fig 3 The proportion of treatments over time (A: total, B: <35, C: 35-, D: 45-)*/
%macro loop_years_Frequency;
%do year=2016 %to 2024;
proc surveyfreq data=demo2;
    where age5=2 and year="&year.";/*修改pgdp=2和后面文件名生成bar图*/
    tables sszx/ cl;
    ods output OneWay=freqout;
run;
data OneWay&year.;
     set freqout;
	 if sszx=" " then delete;
     keep sszx Frequency Percent;
run;
%end;
%mend;
%loop_years_Frequency;
data all_oneway;
set oneway2016-oneway2024 indsname=dsname;  /* 获取数据集名称 */
length dsname_part $32;                    /* 存储数据集名部分 */
dsname_part = scan(dsname, -1, '.');       /* 提取数据集名（去掉库名） */
year = input(substr(dsname_part, 7), 4.);  /* 提取年份并转换为数值 */
Percent=round(Percent,0.01);
format Percent 7.2;
keep sszx Frequency Percent year;                    /* 保留所需变量 */
rename sszx=Group;
run;
data all_oneway;
    set all_oneway;
    /* 将格式值映射到新的排序顺序 */
    if Group = 2 then order = 5;
    else if Group = 1 then order = 3;
    else if Group = 3 then order = 4;
    else if Group = 9 then order = 1;
    else if Group = 4 then order = 7;
    else if Group = 5 then order = 2;
    else if Group = 7 then order = 6;
run;
proc sort data=all_oneway;
    by year order;
run;
/*绘制堆叠式竖图vbar;横图hbar*/
ods listing gpath="D:\博士\博二\邱正西\Fig" image_dpi=300;
ods graphics / imagename="fig3_D-" outputfmt=png width=8in height=6in border=off;
proc sgplot data=all_oneway pctlevel=group dattrmap=myattrmap1;
vbar year / group=Group /*分组变量*/
     grouporder=data
     groupdisplay=stack /*堆叠图*/
     attrid=myid
	 response=Percent
     seglabel seglabelattrs=(Family=Arial color=white size=10 weight=bold);
	 title ' ';
     xaxis label='Year' labelattrs=(size=16) valueattrs=(size=16);
     yaxis label='Percent (%)' grid labelattrs=(size=16) valueattrs=(size=16);
run;
ods graphics / reset;
ods listing close;

/*Fig 6 LOS of UFs treatment over time;Fig 7 Expense of UFs treatment over time*/
/*住院天数均值*/
proc sql;
 create table zyts_sum as
 select 
    sszx as Group,
    year as year1, 
    mean(zyts) as zyts1
 from 
    demo2
group by 
     year,sszx
;
quit;

ods listing gpath="D:\博士\博二\邱正西\Fig" image_dpi=300;
ods graphics / imagename="fig6_2" outputfmt=png width=8in height=6in border=off;
proc sgplot data=zyts_sum dattrmap=myattrmap;
    series x=year1 y=zyts1 / group=Group attrid=myid
    lineattrs=(thickness=2 pattern=solid) 
    markers markerattrs=(size=12 symbol=CIRCLEFILLED); /*datalabel=zyts1;*/
	title" ";
    xaxis label="Year" labelattrs=(size=16) valueattrs=(size=16) values=(2016 to 2024 by 1);
    yaxis label="Days of Hospitalization" labelattrs=(size=16) valueattrs=(size=16) values=(0 to 17 by 1);
    keylegend/ location=inside position=topleft down=2;
run;
ods graphics / reset;
ods listing close;

proc means data=demo2 noprint;
   class sszx;
   var ZYTS;
   output out=stats mean=mean std=std;
run;
data stats;set stats;mean=round(mean,0.001);format mean std 8.3;run;
/* 创建均值bar */
ods listing gpath="D:\博士\博二\邱正西\Fig" image_dpi=300;
ods graphics / imagename="fig6_1_" outputfmt=png width=8in height=6in border=off;
proc sgplot data=stats;
   vbar sszx/response=mean 
   attrid=myid
   datalabel=mean barwidth=0.5 
   datalabelattrs=(color=green size=10 Family=NEWRoman style=NORMAL weight=bold);
   xaxis values=(1,2,3,4,9,5,7) label='Treatment Pattern'labelattrs=(size=16) valueattrs=(size=16);
   yaxis label='Days of Hospitalization' labelattrs=(size=16) valueattrs=(size=16);
run;
ods graphics / reset;
ods listing close;
/*计算次均总费用*/
proc sql;
 create table cjzfy_sum as
 select 
    sszx as Group,
    year as year1, 
    sum(ZFY0) as ZFY1,
    count(sszx) as ssrc, 
    calculated ZFY1 / calculated ssrc as cjzfy  /* 计算次均费用 */
 from 
    demo2
 group by 
     year,sszx
;
quit;

ods listing gpath="D:\博士\博二\邱正西\Fig" image_dpi=300;
ods graphics / imagename="fig7_" outputfmt=png width=8in height=6in border=off;
proc sgplot data=cjzfy_sum dattrmap=myattrmap;
    series x=year1 y=cjzfy / group=Group attrid=myid
    lineattrs=(thickness=2 pattern=solid) 
    markers markerattrs=(size=12 symbol=CIRCLEFILLED); 
/*datalabel=cjzfy;显示*/
	title" ";
    xaxis label="Year" values=(2016 to 2024 by 1) labelattrs=(size=16) valueattrs=(size=16);
    yaxis label="Average cost of hospitalization" values=(3000 to 29000 by 1000) valuesformat=kformat. labelattrs=(size=16) valueattrs=(size=16);
    keylegend/ location=inside position=topleft down=3;
run;
ods graphics / reset;
ods listing close;

/********************************预测数据处理*/
%macro loop_years_Frequency;
%do year=2016 %to 2024;
proc surveyfreq data=demo1;
    where age5=0 and year="&year.";
    tables sszx/ cl;
    ods output OneWay=freqout;
run;
data OneWay&year.;
     set freqout;
	 if sszx=" " then delete;
     keep sszx Frequency Percent;
run;
%end;
%mend;
%loop_years_Frequency;
data all_oneway0;
set oneway2016-oneway2024 indsname=dsname;  /* 获取数据集名称 */
length dsname_part $32;                    /* 存储数据集名部分 */
dsname_part = scan(dsname, -1, '.');       /* 提取数据集名（去掉库名） */
year = input(substr(dsname_part, 7), 4.);  /* 提取年份并转换为数值 */
Percent=round(Percent,0.01);
format Percent 8.2;
agegroup="<34";
keep agegroup sszx Frequency year Percent;                    /* 保留所需变量 */
rename sszx=Group;
run;

%macro loop_years_Frequency;
%do year=2016 %to 2024;
proc surveyfreq data=demo1;
    where age5=1 and year="&year.";
    tables sszx/ cl;
    ods output OneWay=freqout;
run;
data OneWay&year.;
     set freqout;
	 if sszx=" " then delete;
     keep sszx Frequency Percent;
run;
%end;
%mend;
%loop_years_Frequency;
data all_oneway1;
set oneway2016-oneway2024 indsname=dsname;  /* 获取数据集名称 */
length dsname_part $32;                    /* 存储数据集名部分 */
dsname_part = scan(dsname, -1, '.');       /* 提取数据集名（去掉库名） */
year = input(substr(dsname_part, 7), 4.);  /* 提取年份并转换为数值 */
Percent=round(Percent,0.01);
format Percent 8.2;
agegroup="34-44";
keep agegroup sszx Frequency year Percent;                    /* 保留所需变量 */
rename sszx=Group;
run;

%macro loop_years_Frequency;
%do year=2016 %to 2024;
proc surveyfreq data=demo1;
    where age5=2 and year="&year.";
    tables sszx/ cl;
    ods output OneWay=freqout;
run;
data OneWay&year.;
     set freqout;
	 if sszx=" " then delete;
     keep sszx Frequency Percent;
run;
%end;
%mend;
%loop_years_Frequency;
data all_oneway2;
set oneway2016-oneway2024 indsname=dsname;  /* 获取数据集名称 */
length dsname_part $32;                    /* 存储数据集名部分 */
dsname_part = scan(dsname, -1, '.');       /* 提取数据集名（去掉库名） */
year = input(substr(dsname_part, 7), 4.);  /* 提取年份并转换为数值 */
Percent=round(Percent,0.01);
format Percent 8.2;
agegroup="45-";
keep agegroup sszx Frequency year Percent;                    /* 保留所需变量 */
rename sszx=Group;
run;

data combined;
set all_oneway0 all_oneway1 all_oneway2;
run;


/*************************10.13 mixed广义线性混合效应模型*****************************************/
/* 模拟数据生成 - 根据您的数据结构创建示例数据集 */
data demo3;set demo2;
if sszx=4 or sszx=10 or sszx=11 then sszx=12;
year_num = input(year, 4.);
time = year_num - 2016; 
keep year time yydj2 yydj3 yydj4 sszx age5 ZYTS ZFY0;
run;
proc format;
   value otherfmt
   1 = 'HM'
   2 = 'LM'
   3 = 'AM'
   9='FUAS'
   12="Other";
run;
data demo3;set demo3;format sszx otherfmt.;run;
/* LOS的混合效应模型分析 */
ods trace on;
ods output SolutionF=los_solution_ZYTS1;
proc mixed data=demo3 method=reml;
    class yydj2(ref="0") yydj3(ref="0") yydj4(ref="0") sszx(ref="LM") age5(ref="age<35");
    model ZYTS =sszx time sszx*time yydj2 yydj3 yydj4 age5/solution;
/*	lsmeans sszx time sszx*time/cl diff;*/
run;
ods trace off;
/* Expenses的混合效应模型分析 */

ods output SolutionF=los_solution_ZYTS;
proc mixed data=demo3 method=reml;
    class time(ref="3") yydj2(ref="0") sszx(ref="LM") age5(ref="age<35");
    model ZYTS =sszx time sszx*time yydj2 age5/solution;
/*lsmeans sszx time sszx*time/cl diff;*/
run;


ods output SolutionF=los_solution_ZFY;
proc mixed data=demo3 method=reml;
    class yydj2(ref="0") yydj3(ref="0") yydj4(ref="0") sszx(ref="LM") age5(ref="age<35");
    model ZFY0 =sszx time sszx*time yydj2 yydj3 yydj4 age5/solution;
/*lsmeans sszx time sszx*time/cl diff;*/
run;


/***保子宫折线图****/
proc sql;
 create table zyts_sum as
 select 
    sszx as Group,
    year as year1, 
    mean(zyts) as zyts1
 from 
    demo3
group by 
     year,sszx
;
quit;


ods listing gpath="D:\qs_paper\Fig" image_dpi=300;
ods graphics / imagename="fig8_" outputfmt=png width=8in height=6in border=off;
proc sgplot data=zyts_sum dattrmap=myattrmap;
    series x=year1 y=zyts1 / group=Group attrid=myid
    lineattrs=(thickness=2 pattern=solid) 
    markers markerattrs=(size=12 symbol=CIRCLEFILLED) datalabel=zyts1;
	title" ";
    xaxis label="Year" values=(2016 to 2024 by 1);
    yaxis label="Days" values=(3 to 11 by 1);
    keylegend/ location=inside position=topleft down=2;
run;
ods graphics / reset;
ods listing close;

/*构建fuas时间序列需要的数据集*/
/*计算每月出院人数plot1*/
proc sql;
    create table plot1 as
    select 
        fuas as group,
        year1,
        count(*) as freq
    from demo1
    group by fuas, year1
    order by fuas, year1;
quit;
data plot1;
    set plot1;
	/* 将字符串转换为SAS日期（假设格式为YYYY.MM） */
    date = input(compress(year1, '.'), yymmn6.);
    format date yymmn6.;
	/* 设置分界点（2022年1月） */
    if date < '01JAN2022'd then before = 1;
    else before = 0;
    drop date;
run;

proc means data=plot1 mean std min max n maxdec=3;
    var freq;
    class before group;
run;
/* BY语句对group分别进行t检验 */
proc ttest data=plot1;
    by group;           
    class before;       
    var freq;
run;

/*计算ALOS-plot2*/
proc sql;
    create table plot2 as
    select 
        fuas as group,
        year1,
        avg(ZYTS) as ALOS
    from demo1
    group by fuas, year1
    order by fuas, year1;
quit;
data plot2;
    set plot2;
	/* 将字符串转换为SAS日期（假设格式为YYYY.MM） */
    date = input(compress(year1, '.'), yymmn6.);
    format date yymmn6.;
	/* 设置分界点（2022年1月） */
    if date < '01JAN2022'd then before = 1;
    else before = 0;
    drop date;
run;
proc means data=plot2 maxdec=3;         
    class before group;       
    var ALOS;
run;
proc ttest data=plot2;
    by group;           
    class before;       
    var ALOS;
run;

/*计算"inpatient subaverage cost"-plot3*/
proc sql;
    create table plot3 as
    select 
        fuas as group,
        year1,
        sum(ZFY0) as ZFY1,
        count(fuas) as ssrc, 
        calculated ZFY1 / calculated ssrc as cjzfy  /* 计算次均费用 */
    from demo1
    group by fuas, year1
    order by fuas, year1;
quit;
data plot3;
    set plot3;
	/* 将字符串转换为SAS日期（假设格式为YYYY.MM） */
    date = input(compress(year1, '.'), yymmn6.);
    format date yymmn6.;
	/* 设置分界点（2022年1月） */
    if date < '01JAN2022'd then before = 1;
    else before = 0;
    drop date;
run;
proc means data=plot3 maxdec=3;         
    class before group;       
    var cjzfy;
run;
proc ttest data=plot3;
    by group;           
    class before;       
    var cjzfy;
run;


/*构建tr所需数据*/
proc sql;
    create table plot1 as
    select 
        tr as group,
        year1,
        count(*) as freq
    from demo1
    group by tr, year1
    order by tr, year1;
quit;
data plot1;
    set plot1;
	/* 将字符串转换为SAS日期（假设格式为YYYY.MM） */
    date = input(compress(year1, '.'), yymmn6.);
    format date yymmn6.;
	/* 设置分界点（2022年1月） */
    if date < '01JAN2022'd then before = 1;
    else before = 0;
    drop date;
run;

proc means data=plot1 mean std min max n maxdec=3;
    var freq;
    class before group;
run;
/* BY语句对group分别进行t检验 */
proc ttest data=plot1;
    by group;           
    class before;       
    var freq;
run;

/*计算ALOS-plot2*/
proc sql;
    create table plot2 as
    select 
        tr as group,
        year1,
        avg(ZYTS) as ALOS
    from demo1
    group by tr, year1
    order by tr, year1;
quit;
data plot2;
    set plot2;
	/* 将字符串转换为SAS日期（假设格式为YYYY.MM） */
    date = input(compress(year1, '.'), yymmn6.);
    format date yymmn6.;
	/* 设置分界点（2022年1月） */
    if date < '01JAN2022'd then before = 1;
    else before = 0;
    drop date;
run;

proc ttest data=plot2;
    by group;           
    class before;       
    var ALOS;
run;

/*计算"inpatient subaverage cost"-plot3*/
proc sql;
    create table plot3 as
    select 
        tr as group,
        year1,
        sum(ZFY0) as ZFY1,
        count(fuas) as ssrc, 
        calculated ZFY1 / calculated ssrc as cjzfy  /* 计算次均费用 */
    from demo1
    group by tr, year1
    order by tr, year1;
quit;
data plot3;
    set plot3;
	/* 将字符串转换为SAS日期（假设格式为YYYY.MM） */
    date = input(compress(year1, '.'), yymmn6.);
    format date yymmn6.;
	/* 设置分界点（2022年1月） */
    if date < '01JAN2022'd then before = 1;
    else before = 0;
    drop date;
run;
proc means data=plot3 mean std clm maxdec=3;         
    class before group;       
    var cjzfy;
run;
proc ttest data=plot3;
    by group;           
    class before;       
    var cjzfy;
run;

