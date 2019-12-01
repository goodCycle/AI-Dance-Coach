import math

class AvgDistance:
    def __init__(self, keypoints_a, keypoints_b):
        # Analyze for detecting one person
        self.a = keypoints_a[0]
        self.b = keypoints_b[0]
    
    def calculate(self):
        count = min(len(self.a), len(self.b))
        sum = 0
        for p in range(count):
            p_a = self.a[p]
            p_b = self.b[p]
            sum += math.sqrt((p_a[0] - p_b[0])**2 + (p_a[1] - p_b[1])**2)
        return sum/count
