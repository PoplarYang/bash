#!/bin/sh
# 模拟进度条

# 步长
step=2
# 单个填充物
filter="#"
# 填充物
filters=''

for (( i=0; $i<=100; i+=$step )); do
    # 格式化显示
    printf "progress:[%-50s]%d%%\r" $filters $i
    sleep 0.1
    # 填充物增加
    filters=$filter$filters
done
# 结束后，换行
echo
