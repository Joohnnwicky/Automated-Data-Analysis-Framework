"""
天猫母婴交易历史数据 - 统计分析报告生成器
基于Fathom科研方法风格
"""

import pandas as pd
import numpy as np
from scipy import stats
from collections import Counter
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Cross-platform path construction
DATA_DIR = Path(__file__).parent.parent.parent / 'data'
OUTPUT_DIR = Path(__file__).parent.parent.parent / 'output'

# Read data
data_file = DATA_DIR / 'sam_tianchi_mum_baby_trade_history.csv'
if data_file.exists():
    df = pd.read_csv(data_file)
    logger.info(f'Loaded dataset: {len(df)} rows, {len(df.columns)} columns')
else:
    logger.warning(f'Data file not found: {data_file}')
    # Fallback for development - check original location
    fallback = Path.home() / 'Downloads' / '(sample)sam_tianchi_mum_baby_trade_history.csv'
    if fallback.exists():
        df = pd.read_csv(fallback)
        logger.info(f'Loaded from fallback: {fallback}')
    else:
        raise FileNotFoundError(f'Cannot find data file at {data_file} or {fallback}')

# ============================================
# Phase 1: 数据理解
# ============================================
logger.info("=" * 60)
logger.info("Phase 1: 数据理解")
logger.info("=" * 60)

data_overview = {
    "总记录数": len(df),
    "字段数": len(df.columns),
    "字段列表": list(df.columns),
    "时间范围": f"{df['day'].min()} 至 {df['day'].max()}"
}

logger.info(f"数据维度: {len(df)}行 × {len(df.columns)}列")
logger.info(f"字段: {list(df.columns)}")
logger.info(f"时间跨度: {df['day'].min()} - {df['day'].max()}")

# ============================================
# 1. 数据质量评估
# ============================================
logger.info("")
logger.info("=" * 60)
logger.info("一、数据质量评估")
logger.info("=" * 60)

# 1.1 缺失值检查
missing_analysis = {}
for col in df.columns:
    missing_count = df[col].isnull().sum()
    missing_pct = missing_count / len(df) * 100
    missing_analysis[col] = {
        "缺失数量": int(missing_count),
        "缺失比例": round(missing_pct, 4)
    }

logger.info("1.1 缺失值检查")
for col, info in missing_analysis.items():
    logger.info(f"  {col}: 缺失{info['缺失数量']} ({info['缺失比例']}%)")

total_missing = sum([m['缺失数量'] for m in missing_analysis.values()])
missing_score = 100 - (total_missing / (len(df) * len(df.columns)) * 100)

# 1.2 重复记录检查
logger.info("1.2 重复记录检查")
duplicate_rows = df.duplicated().sum()
key_duplicates = df.duplicated(subset=['user_id', 'auction_id', 'day']).sum()

logger.info(f"  完全重复记录: {duplicate_rows}")
logger.info(f"  关键字段重复(user_id+auction_id+day): {key_duplicates}")
duplicate_score = 100 - (duplicate_rows / len(df) * 100)

# 1.3 字段格式一致性
logger.info("1.3 字段格式一致性验证")
format_checks = {
    "user_id整数型": df['user_id'].dtype == np.int64,
    "auction_id整数型": df['auction_id'].dtype == np.int64,
    "buy_mount整数型": df['buy_mount'].dtype == np.int64,
    "dayYYYYMMDD格式": df['day'].astype(str).str.match(r'^\d{8}$').all(),
    "cat_id整数型": df['cat_id'].dtype == np.int64,
    "cat1整数型": df['cat1'].dtype == np.int64
}

format_score = 100 if all(format_checks.values()) else 85
logger.info(f"  格式一致性: {all(format_checks.values())}")

# 综合评分
overall_quality = (missing_score * 0.4 + duplicate_score * 0.3 + format_score * 0.3)
logger.info(f"综合数据质量评分: {overall_quality:.2f}/100")

# ============================================
# 2. 异常值分析
# ============================================
logger.info("")
logger.info("=" * 60)
logger.info("二、异常值分析 (IQR方法)")
logger.info("=" * 60)

buy_mount_stats = {
    "均值": round(df['buy_mount'].mean(), 2),
    "中位数": int(df['buy_mount'].median()),
    "标准差": round(df['buy_mount'].std(), 2),
    "最小值": int(df['buy_mount'].min()),
    "最大值": int(df['buy_mount'].max()),
    "众数": int(df['buy_mount'].mode().values[0])
}

logger.info("购买量统计摘要")
for k, v in buy_mount_stats.items():
    logger.info(f"  {k}: {v}")

# IQR方法
Q1 = df['buy_mount'].quantile(0.25)
Q3 = df['buy_mount'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

logger.info(f"IQR异常值检测:")
logger.info(f"  Q1: {Q1}, Q3: {Q3}, IQR: {IQR}")
logger.info(f"  正常范围: [{lower_bound}, {upper_bound}]")

outliers_high = df[df['buy_mount'] > upper_bound]
outlier_count = len(outliers_high)
outlier_pct = outlier_count / len(df) * 100

logger.info(f"  异常值数量: {outlier_count} ({outlier_pct:.2f}%)")

# 极端值分析
extreme_thresholds = [10, 20, 30, 50, 100]
extreme_analysis = {}
for thresh in extreme_thresholds:
    extreme_count = len(df[df['buy_mount'] >= thresh])
    extreme_analysis[thresh] = {
        "数量": extreme_count,
        "比例": round(extreme_count / len(df) * 100, 2)
    }

logger.info("极端值分级:")
for thresh, info in extreme_analysis.items():
    logger.info(f"  >= {thresh}件: {info['数量']}条 ({info['比例']}%)")

# ============================================
# 3. 分布特征分析
# ============================================
logger.info("")
logger.info("=" * 60)
logger.info("三、分布特征分析")
logger.info("=" * 60)

# 3.1 幂律分布检验
logger.info("3.1 幂律分布检验")
buy_values = df['buy_mount'].values
unique_vals = np.unique(buy_values)
freq = np.array([np.sum(buy_values == v) for v in unique_vals])

# 只对>0的值做log变换
valid_idx = unique_vals > 0
log_vals = np.log10(unique_vals[valid_idx])
log_freq = np.log10(freq[valid_idx])

slope, intercept, r_value, p_value, std_err = stats.linregress(log_vals, log_freq)

power_law_result = {
    "幂指数": round(-slope, 3),
    "R_squared": round(r_value**2, 3),
    "p值": round(p_value, 4),
    "符合幂律": r_value**2 > 0.8 and p_value < 0.05
}

logger.info(f"  幂指数(alpha): {-slope:.3f}")
logger.info(f"  R²: {r_value**2:.3f}")
logger.info(f"  p值: {p_value:.4f}")
logger.info(f"  结论: {'近似幂律分布' if power_law_result['符合幂律'] else '不完全符合幂律'}")

# 3.2 用户购买频次分布
logger.info("3.2 用户购买频次分布")
user_freq = df.groupby('user_id').size()

freq_stats = {
    "总用户数": len(user_freq),
    "平均购买次数": round(user_freq.mean(), 2),
    "中位数": int(user_freq.median()),
    "最大购买次数": int(user_freq.max())
}

logger.info(f"  总用户数: {len(user_freq)}")
logger.info(f"  平均购买次数: {user_freq.mean():.2f}")
logger.info(f"  最大购买次数: {user_freq.max()}")

# 购买频次分布
freq_distribution = {}
freq_counts = user_freq.value_counts().sort_index()
for freq_val in range(1, min(15, freq_counts.index.max()) + 1):
    count = freq_counts.get(freq_val, 0)
    pct = count / len(user_freq) * 100
    freq_distribution[freq_val] = {"用户数": int(count), "比例": round(pct, 2)}

single_purchase = (user_freq == 1).sum()
multi_purchase = (user_freq > 1).sum()
logger.info(f"  单次购买用户: {single_purchase} ({single_purchase/len(user_freq)*100:.2f}%)")
logger.info(f"  多次购买用户: {multi_purchase} ({multi_purchase/len(user_freq)*100:.2f}%)")

# 3.3 类别分布
logger.info("3.3 类别分布特征")
cat1_dist = df['cat1'].value_counts()
cat_dist = df['cat_id'].value_counts()

logger.info(f"  一级类别数: {len(cat1_dist)}")
logger.info(f"  二级类别数: {len(cat_dist)}")

# 类别分布
cat1_distribution = {}
for cat, count in cat1_dist.items():
    pct = count / len(df) * 100
    cat1_distribution[int(cat)] = {"数量": int(count), "比例": round(pct, 2)}

# Herfindahl指数
cat1_share = cat1_dist / len(df)
HHI = float((cat1_share ** 2).sum())

logger.info(f"  Herfindahl指数: {HHI:.4f}")
if HHI > 0.15:
    logger.info(f"  结论: 市场高度集中")
elif HHI > 0.1:
    logger.info(f"  结论: 市场中度集中")
else:
    logger.info(f"  结论: 市场分散")

# ============================================
# 4. 时间序列分析
# ============================================
logger.info("")
logger.info("=" * 60)
logger.info("四、时间序列分析")
logger.info("=" * 60)

# 日期处理
df['date'] = pd.to_datetime(df['day'], format='%Y%m%d')
df['year_month'] = df['date'].dt.to_period('M')

# 月度汇总
monthly_sales = df.groupby('year_month')['buy_mount'].sum()
monthly_orders = df.groupby('year_month').size()

logger.info(f"时间范围: {df['date'].min()} 至 {df['date'].max()}")
logger.info(f"月份数: {len(monthly_sales)}")

monthly_data = []
for period in monthly_sales.index:
    monthly_data.append({
        "月份": str(period),
        "购买量": int(monthly_sales[period]),
        "订单数": int(monthly_orders[period])
    })

# 4.2 趋势平稳性检验
logger.info("4.2 趋势平稳性检验")
monthly_values = monthly_sales.values
time_index = np.arange(len(monthly_values))
slope_t, intercept_t, r_t, p_t, se_t = stats.linregress(time_index, monthly_values)

trend_result = {
    "趋势斜率": round(slope_t, 3),
    "R_squared": round(r_t**2, 3),
    "p值": round(p_t, 4),
    "显著趋势": p_t < 0.05,
    "趋势方向": "上升" if slope_t > 0 else "下降" if slope_t < 0 else "平稳"
}

logger.info(f"  线性趋势斜率: {slope_t:.3f}")
logger.info(f"  R²: {r_t**2:.3f}")
logger.info(f"  p值: {p_t:.4f}")
if p_t < 0.05:
    logger.info(f"  结论: 存在显著{trend_result['趋势方向']}趋势")
else:
    logger.info(f"  结论: 趋势不显著，序列平稳")

# 年度汇总
yearly_summary = df.groupby(df['date'].dt.year)['buy_mount'].agg(['sum', 'count', 'mean'])
yearly_data = []
for year in yearly_summary.index:
    yearly_data.append({
        "年份": int(year),
        "总购买量": int(yearly_summary.loc[year, 'sum']),
        "订单数": int(yearly_summary.loc[year, 'count']),
        "平均购买量": round(yearly_summary.loc[year, 'mean'], 2)
    })

# 4.3 周期性分析
logger.info("4.3 周期性识别")

df['weekday'] = df['date'].dt.dayofweek
df['month'] = df['date'].dt.month
df['quarter'] = df['date'].dt.quarter

weekday_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
weekday_sales = df.groupby('weekday')['buy_mount'].sum()

weekday_distribution = []
for i in range(7):
    sales = weekday_sales.get(i, 0)
    pct = sales / weekday_sales.sum() * 100
    weekday_distribution.append({
        "星期": weekday_names[i],
        "购买量": int(sales),
        "比例": round(pct, 2)
    })

month_sales = df.groupby('month')['buy_mount'].sum()
month_distribution = []
for m in range(1, 13):
    sales = month_sales.get(m, 0)
    pct = sales / month_sales.sum() * 100
    month_distribution.append({
        "月份": m,
        "购买量": int(sales),
        "比例": round(pct, 2)
    })

quarter_sales = df.groupby('quarter')['buy_mount'].sum()
quarter_names = ['第一季度', '第二季度', '第三季度', '第四季度']
quarter_distribution = []
for q in range(1, 5):
    sales = quarter_sales.get(q, 0)
    pct = sales / quarter_sales.sum() * 100
    quarter_distribution.append({
        "季度": quarter_names[q-1],
        "购买量": int(sales),
        "比例": round(pct, 2)
    })

# ANOVA检验
weekday_groups = [group['buy_mount'].values for name, group in df.groupby('weekday')]
f_stat_w, f_pval_w = stats.f_oneway(*weekday_groups)

month_groups = [group['buy_mount'].values for name, group in df.groupby('month')]
f_stat_m, f_pval_m = stats.f_oneway(*month_groups)

periodicity_result = {
    "周内周期性": {
        "F统计量": round(f_stat_w, 3),
        "p值": round(f_pval_w, 4),
        "显著": f_pval_w < 0.05
    },
    "月度周期性": {
        "F统计量": round(f_stat_m, 3),
        "p值": round(f_pval_m, 4),
        "显著": f_pval_m < 0.05
    }
}

logger.info(f"  周内ANOVA F={f_stat_w:.3f}, p={f_pval_w:.4f}")
logger.info(f"  月度ANOVA F={f_stat_m:.3f}, p={f_pval_m:.4f}")

# ============================================
# 输出JSON结果
# ============================================
analysis_result = {
    "data_overview": data_overview,
    "quality_assessment": {
        "missing_analysis": missing_analysis,
        "total_missing": total_missing,
        "missing_score": round(missing_score, 2),
        "duplicate_rows": int(duplicate_rows),
        "duplicate_score": round(duplicate_score, 2),
        "format_score": format_score,
        "overall_quality_score": round(overall_quality, 2)
    },
    "outlier_analysis": {
        "statistics": buy_mount_stats,
        "IQR": {
            "Q1": float(Q1),
            "Q3": float(Q3),
            "IQR": float(IQR),
            "upper_bound": float(upper_bound)
        },
        "outlier_count": outlier_count,
        "outlier_pct": round(outlier_pct, 2),
        "extreme_analysis": extreme_analysis
    },
    "distribution_analysis": {
        "power_law": power_law_result,
        "user_frequency": {
            "stats": freq_stats,
            "distribution": freq_distribution,
            "single_purchase_pct": round(single_purchase/len(user_freq)*100, 2),
            "multi_purchase_pct": round(multi_purchase/len(user_freq)*100, 2)
        },
        "category": {
            "cat1_count": len(cat1_dist),
            "cat_count": len(cat_dist),
            "cat1_distribution": cat1_distribution,
            "HHI": HHI,
            "market_concentration": "高度集中" if HHI > 0.15 else "中度集中" if HHI > 0.1 else "分散"
        }
    },
    "time_series": {
        "monthly_data": monthly_data,
        "yearly_data": yearly_data,
        "trend": trend_result,
        "weekday_distribution": weekday_distribution,
        "month_distribution": month_distribution,
        "quarter_distribution": quarter_distribution,
        "periodicity": periodicity_result
    }
}

# 保存JSON - 使用 OUTPUT_DIR
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
output_file = OUTPUT_DIR / 'analysis_result.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(analysis_result, f, ensure_ascii=False, indent=2)

logger.info("")
logger.info("=" * 60)
logger.info("分析完成，结果已保存")
logger.info("=" * 60)
logger.info(f"JSON文件: {output_file}")

# Entry point
if __name__ == '__main__':
    from config.logging_config import setup_logging
    setup_logging(level=logging.INFO)
    print(f"Analysis complete. Output saved to: {output_file}")