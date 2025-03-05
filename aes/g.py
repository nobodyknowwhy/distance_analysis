import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

# 示例数据
data = {
    "Grammar": [1.0, 1.0, 1.5, 3.0, 3.0, 3.0, 3.5, 4.0, 5.0],
    "g_error": [36, 134, 69, 12, 15, 11, 6, 7, 3]
}
dl_sample = pd.DataFrame(data)


def model_func(x, a, b, c):
    return a * np.exp(-b * x) + c


# 准备数据
x_data = dl_sample['g_error'].values
y_data = dl_sample['Grammar'].values

# 拟合非线性回归模型
popt, pcov = curve_fit(model_func, x_data, y_data)

a, b, c = popt

def predict_grammar(g_error):
    return model_func(g_error, a, b, c)

new_g_error = 24
predicted_grammar = predict_grammar(new_g_error)
print(f"对于 g_error = {new_g_error}，预测的 Grammar 分数为: {predicted_grammar:.2f}")
