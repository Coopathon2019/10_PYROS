#!/usr/bin/env python
# coding: utf-8

# In[156]:


import pandas as pd
 
# 取得需要購買的食材和量
def get_manu(cusines, num = 1):  #cusines 要是list, num 要是 int 預設為 1人份

    data = pd.read_csv('cal.csv', index_col=['食材', '單位'])
    data = data[cusines].dropna(how='all').sum(axis=1)
    recipe = dict(data.index)
    
    a = []

    for i, j in zip(list(data),list(recipe.values())):
        if i == -1.0:
            a.append(j) 
        else:    
            a.append(str(round(i*num,2))+' '+j) 
       
    return dict(zip(list(recipe.keys()),a))  # 回傳的是 dict

# 個別菜餚的食譜
def get_recipe(name):  #cusines 要是str
    
    recipe = pd.read_csv('recipe.csv', index_col=['Step']).dropna(how='all')
    return dict(recipe[name].dropna().apply(lambda x: x.split(' ') ))  # 回傳的是 dict


    
def get_nutrition(name):
    return dict(pd.read_json('nutrition.json')[name])


# In[159]:


get_ipython().system('jupyter nbconvert --to script Calories.ipynb')


# In[160]:


get_manu(['泡菜雞肉鴻喜菇', '麻婆豆腐'],3)


# In[161]:


get_recipe('麻婆豆腐')


# In[ ]:




