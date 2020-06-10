# 项目本地部署
## 背景 background
网站规模并不大，暂时没有自动化部署的需求，况且自动化部署反而麻烦；因此写一个脚本，用于在服务器手动部署项目。

## 更新 changelog
v0.1 从旧版本恢复的版本再次更新时会以旧版本为基础进行更新

## 功能 function
### 更新 update
* 执行`python local_deploy.py`,根据提示输入`u`;  
* 首先会备份老版本，备份成功后解压发布新版本;  
* 将新版本写入`last_versions`中；  
* 退出时会进行版本检查，保证一定数量`version_to_keep`的可恢复版本，默认是3个;  
* 可以修改指定的文件权限；

### 恢复 restore
执行`python local_deploy.py`,根据提示输入`r`， 选择可以恢复的版本即可；

### 清理缓存 clear 
执行`python local_deploy.py`,根据提示输入`c`，并清空某些目录，比如php程序中的runtime

## 参数说明
```
last_versions_file = "last_versions"        # 已经更新的并且可以恢复的版本记录
white_versions_file = "white_versions"      # 版本白名单，其中的版本过期也不会清除
version_to_keep = 3                         # 保留的可以恢复的版本数量
file_to_change_owner = []                   # 需要改变文件属主的文件，路径相对于app_root，如'Runtime'
file_to_clear = ['Runtime',]                # 需清理的文件，如缓存'Runtime'，路径相对于app_root，
app_user = 'www'                            # app_root的属主
app_root = "app_root"                       # 网站的根目录连接
update_type = "delta"                       # 是否进行差量更新
```