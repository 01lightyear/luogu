class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (4 * self.n)  # 4倍大小的树
        self.build(data, 0, 0, self.n - 1)
    
    def build(self, data, node, start, end):
        if start == end:
            self.tree[node] = data[start]
        else:
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2
            self.build(data, left_child, start, mid)
            self.build(data, right_child, mid + 1, end)
            self.tree[node] = self.tree[left_child] + self.tree[right_child]
    
    def update(self, idx, val, node, start, end):
        if start == end:
            self.tree[node] = val
        else:
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2
            if start <= idx <= mid:
                self.update(idx, val, left_child, start, mid)
            else:
                self.update(idx, val, right_child, mid + 1, end)
            self.tree[node] = self.tree[left_child] + self.tree[right_child]
    
    def query(self, L, R, node, start, end):
        if R < start or end < L:
            return 0  # 范围外，返回0
        if L <= start and end <= R:
            return self.tree[node]
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        left_result = self.query(L, R, left_child, start, mid)
        right_result = self.query(L, R, right_child, mid + 1, end)
        return left_result + right_result

# 示例
data = [1, 2, 3, 4, 5]
seg_tree = SegmentTree(data)
print(seg_tree.query(1, 3, 0, 0, len(data) - 1))  # 查询区间 [1, 3]
seg_tree.update(2, 6, 0, 0, len(data) - 1)  # 更新索引 2 为 6
print(seg_tree.query(1, 3, 0, 0, len(data) - 1))  # 查询区间 [1, 3] 更新后的结果

class SegmentTreeLazy:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (4 * self.n)      # 线段树存储数据
        self.lazy = [0] * (4 * self.n)      # 懒标记，记录懒惰更新的值
        self.build(data, 0, 0, self.n - 1)  # 初始化线段树
    
    def build(self, data, node, start, end):
        if start == end:
            self.tree[node] = data[start]
        else:
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2
            self.build(data, left_child, start, mid)
            self.build(data, right_child, mid + 1, end)
            self.tree[node] = self.tree[left_child] + self.tree[right_child]
    
    def propagate(self, node, start, end):
        if self.lazy[node] != 0:
            self.tree[node] += (end - start + 1) * self.lazy[node]  # 应用懒标记
            if start != end:
                # 向下传播懒标记到子节点
                self.lazy[2 * node + 1] += self.lazy[node]
                self.lazy[2 * node + 2] += self.lazy[node]
            self.lazy[node] = 0  # 清除当前节点的懒标记
    
    def update_range(self, L, R, val, node, start, end):
        # 首先传播懒标记
        self.propagate(node, start, end)

        if R < start or end < L:  # 当前节点完全不在更新区间内
            return
        if L <= start and end <= R:  # 当前节点完全在更新区间内
            self.tree[node] += (end - start + 1) * val
            if start != end:
                # 向子节点标记懒更新
                self.lazy[2 * node + 1] += val
                self.lazy[2 * node + 2] += val
            return
        
        # 当前节点部分在区间内，递归更新左右子节点
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        self.update_range(L, R, val, left_child, start, mid)
        self.update_range(L, R, val, right_child, mid + 1, end)
        self.tree[node] = self.tree[left_child] + self.tree[right_child]
    
    def query(self, L, R, node, start, end):
        # 传播懒标记
        self.propagate(node, start, end)

        if R < start or end < L:  # 当前节点完全不在查询区间内
            return 0
        if L <= start and end <= R:  # 当前节点完全在查询区间内
            return self.tree[node]
        
        # 当前节点部分在查询区间内，递归查询左右子节点
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        left_result = self.query(L, R, left_child, start, mid)
        right_result = self.query(L, R, right_child, mid + 1, end)
        return left_result + right_result

# 示例
data = [1, 2, 3, 4, 5]
seg_tree_lazy = SegmentTreeLazy(data)

# 区间 [1, 3] 加 2
seg_tree_lazy.update_range(1, 3, 2, 0, 0, len(data) - 1)

# 查询区间 [1, 3]
print(seg_tree_lazy.query(1, 3, 0, 0, len(data) - 1))

# 区间 [2, 4] 加 3
seg_tree_lazy.update_range(2, 4, 3, 0, 0, len(data) - 1)

# 查询区间 [1, 3]
print(seg_tree_lazy.query(1, 3, 0, 0, len(data) - 1))
