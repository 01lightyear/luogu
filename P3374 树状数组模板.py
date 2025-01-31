class FenwickTree:
    def __init__(self, size):
        self.n = size
        self.tree = [0] * (self.n + 1)  # 树状数组使用 1-based 索引
    
    def update(self, index, delta):
        """将原数组 index (0-based) 处的值增加 delta"""
        i = index + 1  # 转换为 1-based 索引
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i
    
    def query(self, index):
        """查询原数组前 index+1 个元素的和 (0-based 的 index)"""
        res = 0
        i = index + 1  # 转换为 1-based 索引
        while i > 0:
            res += self.tree[i]
            i -= i & -i
        return res
    
    def query_range(self, l, r):
        """查询原数组闭区间 [l, r] (0-based) 的和"""
        return self.query(r) - (self.query(l - 1) if l > 0 else 0)