# CodeCraft
CodeCraft2019初赛题目

## 判题器
判题器写的没有poi大神写得好，主要的差异是我的有些死锁情况判不出来（不清楚原因...）

### 图形化界面（game模块）

![image]
(https://github.com/Lazy-Pig/CodeCraft/blob/master/%E5%88%A4%E9%A2%98%E5%99%A8%E5%9B%BE%E5%BD%A2%E5%8C%96%E7%A4%BA%E4%BE%8B.gif)

有图形化界面，主要是src中的game模块，基于pygame框架写的，判题器的具体特点：
- 只能显示某个指定路口的详细路况，即每个tick每个车道上行驶的车辆的id号
- 固定显示每个road的3个车道（默认每个路口都是双向，正反各3个车道）
- 固定显示每个车道的10个槽位
- 这些限制只是为了方便图形化显示的限制，判题器的运行更新逻辑没有这样的限制的

## 调度器
迪杰斯特拉提前规划每辆车的路线，后期用广度优先搜索打了一个补丁，解决非强连通图最短路径的问题
