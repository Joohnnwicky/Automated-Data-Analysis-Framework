#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
母婴交易数据概览分析
"""

import pandas as pd
import numpy as np
import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

# Cross-platform path construction
DATA_DIR = Path(__file__).parent.parent.parent / 'data'
OUTPUT_DIR = Path(__file__).parent.parent.parent / 'output'

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

# 基础统计
stats = {
    "总交易记录": len(df),
    "唯一用户数": df['user_id'].nunique(),
    "唯一商品数": df['auction_id'].nunique(),
    "一级类别数": df['cat1'].nunique(),
    "二级类别数": df['cat_id'].nunique(),
    "总购买量": int(df['buy_mount'].sum()),
    "平均购买量": round(df['buy_mount'].mean(), 2),
    "购买量中位数": int(df['buy_mount'].median()),
    "购买量标准差": round(df['buy_mount'].std(), 2),
    "最大购买量": int(df['buy_mount'].max()),
    "最小购买量": int(df['buy_mount'].min())
}

# 日期处理
df['day'] = pd.to_datetime(df['day'], format='%Y%m%d')
df['year'] = df['day'].dt.year
df['month'] = df['day'].dt.month
df['year_month'] = df['day'].dt.to_period('M').astype(str)

stats["时间范围"] = f"{df['day'].min().strftime('%Y-%m-%d')} 至 {df['day'].max().strftime('%Y-%m-%d')}"

# 购买量分布
buy_dist = df['buy_mount'].value_counts().head(10).to_dict()
stats["购买量分布top10"] = buy_dist

# 单件购买占比
single_pct = (df['buy_mount'] == 1).sum() / len(df) * 100
stats["单件购买占比"] = round(single_pct, 1)

# 极端购买（>100）
extreme_count = (df['buy_mount'] > 100).sum()
extreme_users = df[df['buy_mount'] > 100]['user_id'].nunique()
stats["极端购买次数(>100)"] = extreme_count
stats["极端购买用户数"] = extreme_users

# 10000件购买
max_buy_count = (df['buy_mount'] == 10000).sum()
stats["购买量=10000次数"] = max_buy_count

# 月度购买趋势
monthly = df.groupby('year_month')['buy_mount'].sum().to_dict()
stats["月度购买量"] = monthly

# 11月数据（双十一）
nov_data = df[df['month'] == 11]
nov_stats = nov_data.groupby('year').agg({
    'buy_mount': ['sum', 'count']
}).reset_index()
nov_stats.columns = ['year', 'sum', 'count']
stats["11月购买统计"] = nov_stats.to_dict('records')

# 用户复购分析
user_orders = df.groupby('user_id').size()
single_order_users = (user_orders == 1).sum()
multi_order_users = (user_orders >= 2).sum()
stats["单次购买用户数"] = single_order_users
stats["复购用户数"] = multi_order_users
stats["复购率"] = round(multi_order_users / len(user_orders) * 100, 1)

# 类别分析
cat1_stats = df.groupby('cat1').agg({
    'buy_mount': ['sum', 'count', 'mean']
}).reset_index()
cat1_stats.columns = ['cat1', 'total_buy', 'order_count', 'avg_buy']
cat1_stats = cat1_stats.sort_values('total_buy', ascending=False).head(10)
stats["一级类别购买top10"] = cat1_stats.to_dict('records')

# Output JSON - user-facing output uses print()
print(json.dumps(stats, ensure_ascii=False, indent=2))

# Entry point
if __name__ == '__main__':
    from config.logging_config import setup_logging
    setup_logging(level=logging.INFO)
    # JSON output is handled by print() above