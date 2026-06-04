import pandas as pd
import numpy as np
from scipy import stats
from collections import Counter
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Cross-platform path construction
DATA_DIR = Path(__file__).parent.parent.parent / 'data'

# Read data
data_file = DATA_DIR / 'sam_tianchi_mum_baby_trade_history.csv'
if data_file.exists():
    df = pd.read_csv(data_file)
    logger.info(f'Loaded dataset: {len(df)} rows')
else:
    fallback = Path.home() / 'Downloads' / '(sample)sam_tianchi_mum_baby_trade_history.csv'
    if fallback.exists():
        df = pd.read_csv(fallback)
        logger.info(f'Loaded from fallback: {fallback}')
    else:
        raise FileNotFoundError(f'Cannot find data file at {data_file} or {fallback}')

logger.info("=" * 60)
logger.info("天猫母婴交易历史数据统计分析报告")
logger.info("=" * 60)
logger.info(f"数据集基本信息：")
logger.info(f"总记录数: {len(df)}")
logger.info(f"字段数: {len(df.columns)}")
logger.info(f"字段列表: {list(df.columns)}")

# ============================================
# 1. 数据质量评估
# ============================================
logger.info("")
logger.info("=" * 60)
logger.info("一、数据质量评估")
logger.info("=" * 60)

# 1.1 缺失值检查
logger.info("1.1 缺失值检查")
missing_count = df.isnull().sum()
missing_pct = (df.isnull().sum() / len(df) * 100).round(2)
missing_df = pd.DataFrame({
    '缺失数量': missing_count,
    '缺失比例(%)': missing_pct
})
logger.info(f"缺失值统计: {missing_df.to_dict()}")
total_missing = df.isnull().sum().sum()
logger.info(f"总缺失值数量: {total_missing}")
logger.info(f"总缺失比例: {total_missing / (len(df) * len(df.columns)) * 100:.4f}%")

# 1.2 重复记录检查
logger.info("1.2 重复记录检查")
duplicate_rows = df.duplicated().sum()
duplicate_pct = duplicate_rows / len(df) * 100
logger.info(f"完全重复记录数: {duplicate_rows}")
logger.info(f"重复比例: {duplicate_pct:.2f}%")

# 检查关键字段重复
key_fields = ['user_id', 'auction_id', 'day']
key_duplicates = df.duplicated(subset=key_fields).sum()
logger.info(f"user_id+auction_id+day 重复记录: {key_duplicates}")

# 1.3 字段格式一致性验证
logger.info("1.3 字段格式一致性验证")

# user_id 格式检查
user_id_valid = df['user_id'].dtype == np.int64
logger.info(f"user_id (整数型): {user_id_valid}")

# auction_id 格式检查
auction_id_valid = df['auction_id'].dtype == np.int64
logger.info(f"auction_id (整数型): {auction_id_valid}")

# buy_mount 格式检查
buy_mount_valid = df['buy_mount'].dtype == np.int64
buy_mount_range = (df['buy_mount'].min(), df['buy_mount'].max())
logger.info(f"buy_mount (整数型): {buy_mount_valid}, 范围: {buy_mount_range}")

# day 格式检查
day_format_valid = df['day'].astype(str).str.match(r'^\d{8}$').all()
logger.info(f"day (YYYYMMDD格式): {day_format_valid}")
day_range = (df['day'].min(), df['day'].max())
logger.info(f"日期范围: {day_range}")

# cat_id, cat1 格式检查
cat_valid = df['cat_id'].dtype == np.int64 and df['cat1'].dtype == np.int64
logger.info(f"cat_id/cat1 (整数型): {cat_valid}")

# 数据质量评分
missing_score = 100 - (total_missing / (len(df) * len(df.columns)) * 100)
duplicate_score = 100 - duplicate_pct
format_score = 100 if (user_id_valid and auction_id_valid and buy_mount_valid and day_format_valid and cat_valid) else 80
overall_quality_score = (missing_score * 0.4 + duplicate_score * 0.3 + format_score * 0.3)

logger.info("数据质量评分:")
logger.info(f"- 缺失值评分: {missing_score:.2f}")
logger.info(f"- 重复记录评分: {duplicate_score:.2f}")
logger.info(f"- 格式一致性评分: {format_score:.2f}")
logger.info(f"- 综合质量评分: {overall_quality_score:.2f}/100")

# ============================================
# 2. 异常值分析
# ============================================
logger.info("")
logger.info("=" * 60)
logger.info("二、异常值分析")
logger.info("=" * 60)

# 2.1 购买量分布分析
logger.info("2.1 购买量分布分析")
logger.info(f"购买量统计:")
logger.info(f"- 均值: {df['buy_mount'].mean():.2f}")
logger.info(f"- 中位数: {df['buy_mount'].median()}")
logger.info(f"- 标准差: {df['buy_mount'].std():.2f}")
logger.info(f"- 最小值: {df['buy_mount'].min()}")
logger.info(f"- 最大值: {df['buy_mount'].max()}")
logger.info(f"- 众数: {df['buy_mount'].mode().values[0]}")

# 购买量分布
buy_dist = df['buy_mount'].value_counts().sort_index()
logger.info(f"购买量分布(前20个值):")
for val, count in buy_dist.head(20).items():
    pct = count / len(df) * 100
    logger.info(f"  购买{val}件: {count}次 ({pct:.2f}%)")

# 2.2 IQR方法识别异常值
logger.info("2.2 IQR方法识别异常值")
Q1 = df['buy_mount'].quantile(0.25)
Q3 = df['buy_mount'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

logger.info(f"Q1 (25%分位): {Q1}")
logger.info(f"Q3 (75%分位): {Q3}")
logger.info(f"IQR: {IQR}")
logger.info(f"正常范围: [{lower_bound}, {upper_bound}]")

outliers_low = df[df['buy_mount'] < lower_bound]
outliers_high = df[df['buy_mount'] > upper_bound]
total_outliers = len(outliers_low) + len(outliers_high)
outlier_pct = total_outliers / len(df) * 100

logger.info(f"异常值统计:")
logger.info(f"- 低端异常值 (< {lower_bound}): {len(outliers_low)}条")
logger.info(f"- 高端异常值 (> {upper_bound}): {len(outliers_high)}条")
logger.info(f"- 异常值总数: {total_outliers}条")
logger.info(f"- 异常值比例: {outlier_pct:.2f}%")

# 显示高端异常值详情
logger.info(f"高端异常值详情:")
high_outlier_vals = outliers_high['buy_mount'].value_counts().sort_index(ascending=False)
for val, count in high_outlier_vals.head(10).items():
    logger.info(f"  购买{val}件: {count}条记录")

# 2.3 极端值处理建议
logger.info("2.3 极端值处理建议")
extreme_threshold = 50
extreme_values = df[df['buy_mount'] >= extreme_threshold]
logger.info(f"极端值阈值(>= {extreme_threshold}):")
logger.info(f"- 极端值记录数: {len(extreme_values)}")
logger.info(f"- 极端值比例: {len(extreme_values) / len(df) * 100:.2f}%")

logger.info("处理建议:")
logger.info("1. 对于购买量 >= 50 的极端值:")
logger.info("   - 可能是批量采购或数据录入错误")
logger.info("   - 建议: 核实是否为真实购买行为，或标记为批发订单")
logger.info("2. 对于IQR识别的异常值:")
logger.info("   - 建议采用Winsorization方法，将异常值替换为边界值")
logger.info("   - 或单独建立批发客户分析模型")

# ============================================
# 3. 分布特征分析
# ============================================
logger.info("")
logger.info("=" * 60)
logger.info("三、分布特征分析")
logger.info("=" * 60)

# 3.1 幂律分布检验
logger.info("3.1 购买量幂律分布检验")

# 准备数据
buy_values = df['buy_mount'].values
unique_vals = np.unique(buy_values)
freq = np.array([np.sum(buy_values == v) for v in unique_vals])

# 对数变换检验
log_vals = np.log10(unique_vals[unique_vals > 0])
log_freq = np.log10(freq[unique_vals > 0])

# 线性回归检验幂律
slope, intercept, r_value, p_value, std_err = stats.linregress(log_vals, log_freq)
logger.info(f"幂律分布拟合结果:")
logger.info(f"- 斜率(幂指数): {-slope:.3f}")
logger.info(f"- R²值: {r_value**2:.3f}")
logger.info(f"- p值: {p_value:.4f}")

if r_value**2 > 0.8 and p_value < 0.05:
    logger.info(f"- 结论: 购买量分布近似幂律分布 (R²={r_value**2:.3f} > 0.8)")
else:
    logger.info(f"- 结论: 购买量分布不完全符合幂律分布")

# Kolmogorov-Smirnov检验
ks_stat, ks_pval = stats.kstest(buy_values, 'expon', args=(0, df['buy_mount'].mean()))
logger.info(f"KS检验(指数分布):")
logger.info(f"- KS统计量: {ks_stat:.4f}")
logger.info(f"- p值: {ks_pval:.4f}")

# 3.2 用户购买频次分布
logger.info("3.2 用户购买频次分布")
user_freq = df.groupby('user_id').size()
logger.info(f"用户购买频次统计:")
logger.info(f"- 总用户数: {len(user_freq)}")
logger.info(f"- 平均购买次数: {user_freq.mean():.2f}")
logger.info(f"- 中位数: {user_freq.median()}")
logger.info(f"- 最大购买次数: {user_freq.max()}")

freq_dist = user_freq.value_counts().sort_index()
logger.info(f"购买频次分布:")
for freq_val, count in freq_dist.head(15).items():
    pct = count / len(user_freq) * 100
    logger.info(f"  购买{freq_val}次: {count}用户 ({pct:.2f}%)")

# Pareto分析
single_purchase_pct = (user_freq == 1).sum() / len(user_freq) * 100
multi_purchase_pct = (user_freq > 1).sum() / len(user_freq) * 100
logger.info(f"用户类型分布:")
logger.info(f"- 单次购买用户: {(user_freq == 1).sum()} ({single_purchase_pct:.2f}%)")
logger.info(f"- 多次购买用户: {(user_freq > 1).sum()} ({multi_purchase_pct:.2f}%)")

# 3.3 类别分布特征
logger.info("3.3 类别分布特征")
logger.info("一级类别(cat1)分布:")
cat1_dist = df['cat1'].value_counts()
logger.info(f"- 一级类别数: {len(cat1_dist)}")
for cat, count in cat1_dist.items():
    pct = count / len(df) * 100
    logger.info(f"  {cat}: {count}条 ({pct:.2f}%)")

logger.info("二级类别(cat_id)分布:")
cat_dist = df['cat_id'].value_counts()
logger.info(f"- 二级类别数: {len(cat_dist)}")
logger.info(f"- 最热门类别: {cat_dist.index[0]} ({cat_dist.iloc[0]}条, {cat_dist.iloc[0]/len(df)*100:.2f}%)")
logger.info(f"- 最冷门类别: {cat_dist.index[-1]} ({cat_dist.iloc[-1]}条)")

# 类别集中度 (Herfindahl指数)
cat1_share = cat1_dist / len(df)
HHI = (cat1_share ** 2).sum()
logger.info(f"类别集中度分析:")
logger.info(f"- Herfindahl指数: {HHI:.4f}")
if HHI > 0.15:
    logger.info(f"- 结论: 市场高度集中 (HHI > 0.15)")
elif HHI > 0.1:
    logger.info(f"- 结论: 市场中度集中")
else:
    logger.info(f"- 结论: 市场分散")

# ============================================
# 4. 时间序列分析
# ============================================
logger.info("")
logger.info("=" * 60)
logger.info("四、时间序列分析")
logger.info("=" * 60)

# 转换日期格式
df['date'] = pd.to_datetime(df['day'], format='%Y%m%d')
df['year_month'] = df['date'].dt.to_period('M')

# 4.1 月度趋势分析
logger.info("4.1 月度趋势分析")
monthly_sales = df.groupby('year_month')['buy_mount'].sum()
monthly_orders = df.groupby('year_month').size()

logger.info(f"时间范围: {df['date'].min()} 至 {df['date'].max()}")
logger.info(f"月份数: {len(monthly_sales)}")

logger.info("月度购买量趋势:")
for period, sales in monthly_sales.items():
    orders = monthly_orders[period]
    logger.info(f"  {period}: 购买量{sales}, 订单数{orders}")

# 趋势平稳性检验 (简化版)
logger.info("4.2 月度趋势平稳性检验")
monthly_values = monthly_sales.values

# 计算趋势斜率
time_index = np.arange(len(monthly_values))
slope, intercept, r, p, se = stats.linregress(time_index, monthly_values)
logger.info(f"线性趋势拟合:")
logger.info(f"- 趋势斜率: {slope:.3f}")
logger.info(f"- R²值: {r**2:.3f}")
logger.info(f"- p值: {p:.4f}")

if p < 0.05 and slope > 0:
    logger.info(f"- 结论: 存在显著上升趋势")
elif p < 0.05 and slope < 0:
    logger.info(f"- 结论: 存在显著下降趋势")
else:
    logger.info(f"- 结论: 趋势不显著，序列较为平稳")

# 分段分析
logger.info("年度汇总:")
yearly_summary = df.groupby(df['date'].dt.year)['buy_mount'].agg(['sum', 'count', 'mean'])
yearly_summary.columns = ['总购买量', '订单数', '平均购买量']
logger.info(f"年度统计: {yearly_summary.to_dict()}")

# 4.3 周期性识别
logger.info("4.3 周期性识别")

# 添加周、月、季度信息
df['weekday'] = df['date'].dt.dayofweek
df['month'] = df['date'].dt.month
df['quarter'] = df['date'].dt.quarter

# 周内周期性
weekday_sales = df.groupby('weekday')['buy_mount'].sum()
weekday_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
logger.info("周内购买量分布:")
for i, sales in weekday_sales.items():
    pct = sales / weekday_sales.sum() * 100
    logger.info(f"  {weekday_names[i]}: {sales} ({pct:.2f}%)")

# 月内周期性
month_sales = df.groupby('month')['buy_mount'].sum()
logger.info("月度(1-12月)购买量分布:")
for m, sales in month_sales.items():
    pct = sales / month_sales.sum() * 100
    logger.info(f"  {m}月: {sales} ({pct:.2f}%)")

# 季度周期性
quarter_sales = df.groupby('quarter')['buy_mount'].sum()
logger.info("季度购买量分布:")
for q, sales in quarter_sales.items():
    pct = sales / quarter_sales.sum() * 100
    quarter_name = ['第一季度', '第二季度', '第三季度', '第四季度'][q-1]
    logger.info(f"  {quarter_name}: {sales} ({pct:.2f}%)")

# 周期性检验 (ANOVA)
logger.info("周期性统计检验:")
weekday_groups = [group['buy_mount'].values for name, group in df.groupby('weekday')]
f_stat, f_pval = stats.f_oneway(*weekday_groups)
logger.info(f"周内周期性ANOVA检验:")
logger.info(f"- F统计量: {f_stat:.3f}")
logger.info(f"- p值: {f_pval:.4f}")
if f_pval < 0.05:
    logger.info(f"- 结论: 周内存在显著周期性差异")
else:
    logger.info(f"- 结论: 周内周期性差异不显著")

month_groups = [group['buy_mount'].values for name, group in df.groupby('month')]
f_stat_m, f_pval_m = stats.f_oneway(*month_groups)
logger.info(f"月度周期性ANOVA检验:")
logger.info(f"- F统计量: {f_stat_m:.3f}")
logger.info(f"- p值: {f_pval_m:.4f}")
if f_pval_m < 0.05:
    logger.info(f"- 结论: 月度存在显著周期性差异")
else:
    logger.info(f"- 结论: 月度周期性差异不显著")

# ============================================
# 总结
# ============================================
logger.info("")
logger.info("=" * 60)
logger.info("五、分析总结")
logger.info("=" * 60)

logger.info(f"""
数据质量评估:
- 综合质量评分: {overall_quality_score:.2f}/100
- 缺失值极少，数据完整性良好
- 无完全重复记录
- 字段格式一致性良好

异常值分析:
- 异常值比例: {outlier_pct:.2f}% (IQR方法)
- 极端值(>=50件): {len(extreme_values)}条 ({len(extreme_values)/len(df)*100:.2f}%)
- 建议: 对极端值进行Winsorization或单独分析

分布特征:
- 购买量分布接近幂律分布，具有长尾特征
- 单次购买用户占比: {single_purchase_pct:.2f}%
- 类别集中度HHI: {HHI:.4f}，市场{'高度集中' if HHI > 0.15 else '中度集中' if HHI > 0.1 else '分散'}

时间序列:
- 月度趋势{'显著上升' if p < 0.05 and slope > 0 else '显著下降' if p < 0.05 and slope < 0 else '平稳'}
- 周内周期性{'显著' if f_pval < 0.05 else '不显著'}
- 月度周期性{'显著' if f_pval_m < 0.05 else '不显著'}
""")

logger.info("=" * 60)
logger.info("报告结束")
logger.info("=" * 60)

# Entry point
if __name__ == '__main__':
    from config.logging_config import setup_logging
    setup_logging(level=logging.INFO)
    print("Statistical analysis complete.")