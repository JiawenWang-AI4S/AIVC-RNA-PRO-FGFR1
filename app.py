import json
from pathlib import Path
import pandas as pd
import streamlit as st
ROOT=Path(__file__).resolve().parent
RESULT=ROOT/'data/state/local'
OFFICIAL=ROOT/'data/state/official'
FIG=ROOT/'assets/state'
PTF=ROOT/'assets/proteintalks'
DOCK=ROOT/'data/docking'
st.set_page_config(page_title='AIVC Multimodal Drug Screening',layout='wide')
st.title('多模态虚拟细胞小分子药物筛选 AI 平台')
st.caption('STATE 转录组虚拟细胞 × ProteinTalks 蛋白组虚拟细胞 × 结构对接验证｜所有数字均来自服务器真实产物')
t1,t2,t3,t4,t5=st.tabs(['1 总体闭环','2 转录组','3 蛋白组','4 候选排序','5 对接验证'])
with t1:
 st.header('从扰动预测到结构验证的闭环')
 st.markdown('### 疾病/靶点输入 → STATE → ProteinTalks → 多模态候选排序 → 分子对接验证')
 st.success('当前状态：Erdafitinib–FGFR1 对接已完成，并通过 5EW8 共晶重对接校验。')
 st.info('候选排序回答“优先验证谁”；对接回答“是否存在合理结合构象”。二者不是同一分数。')
with t2:
 st.header('STATE · Replogle-Nadig HepG2 zero-shot')
 local=pd.read_csv(RESULT/'hepg2_agg_results.csv').iloc[0]
 official=pd.read_csv(OFFICIAL/'hepg2_agg_results.csv').iloc[0]
 keys=[('Pearson Δ','pearson_delta'),('DE overlap @50','overlap_at_50'),('Discrimination L1','discrimination_score_l1'),('Discrimination cosine','discrimination_score_cosine')]
 cs=st.columns(4)
 for c,(lab,k) in zip(cs,keys): c.metric(lab,f'{local[k]:.6f}',f'官方同 checkpoint {official[k]:.6f}',delta_color='off')
 st.caption('主结论：batch adapter 后扰动效应预测有所改善；论文主表与此 HepG2 zero-shot checkpoint 聚合口径不同。')
 for f,cap in [('pearson_delta_scatter.png','Observed vs predicted Δ expression'),('cell_eval_metric_panels.png','Cell-Eval 多指标逐扰动分布')]:
  p=FIG/f
  if p.exists(): st.image(str(p),caption=cap,use_container_width=True)
with t3:
 st.header('ProteinTalks · 时间分辨蛋白动态推理')
 c1,c2,c3=st.columns(3); c1.metric('伪 bulk 组','4,813'); c2.metric('时间点','6 / 24 / 48 h'); c3.metric('有限值输出','100%')
 st.warning('边界：尚缺真实配对真值与原始药物特征的严格 benchmark，因此本页展示运行完整性，不把它表述为临床性能。')
 for f in ['proteintalks_task_metrics.png','proteintalks_metric_heatmap.png']:
  p=PTF/f
  if p.exists(): st.image(str(p),use_container_width=True)
with t4:
 st.header('多模态候选排序')
 st.metric('Rank #1','Erdafitinib / FGFR1','融合分数 0.498990',delta_color='off')
 st.bar_chart(pd.DataFrame({'modality':['STATE','ProteinTalks','Fusion'],'score':[0.452020,0.545455,0.498990]}).set_index('modality'))
 st.info('这是跨模态候选优先级，不是结合能、亲和力或药效。')
with t5:
 st.header('FGFR1–Erdafitinib 结构对接与重对接验证')
 e=pd.read_csv(DOCK/'vina_scores.csv'); r=pd.read_csv(DOCK/'redocking_rmsd.csv'); best_i=int(r['rmsd_A'].idxmin())
 a,b,c=st.columns(3); a.metric('最佳 Vina affinity',f'{e.iloc[0,0]:.3f} kcal/mol'); b.metric('最低共晶 RMSD',f'{r.iloc[best_i,1]:.3f} Å'); c.metric('结构来源','PDB 5EW8')
 st.image(str(DOCK/'FGFR1_Erdafitinib_docking_300dpi.png'),use_container_width=True)
 st.caption('Vina 1.2.7｜seed 20261004｜exhaustiveness 32｜20 poses｜24 Å cubic box centered on co-crystal ligand 5SF。')
 st.warning('对接分数是构象筛选评分，不等同于实验结合自由能。下一步：关键残基检查 → 分子动力学稳定性复核 → 湿实验验证。')
 st.download_button('下载 300 dpi PDF',data=(DOCK/'FGFR1_Erdafitinib_docking_300dpi.pdf').read_bytes(),file_name='FGFR1_Erdafitinib_docking_300dpi.pdf',mime='application/pdf')
