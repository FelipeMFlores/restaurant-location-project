from typing import List
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_state_distribution(state_count: List):
    df_state_count=pd.DataFrame(state_count, columns =['Name', 'Restaurants']).sort_values(by=['Restaurants'])
    plt.figure(figsize=(10,6))
    plt.title("Number of Chipotle Stores by State")
    sns.barplot(x='Name', y='Restaurants', data=df_state_count)
    plt.xticks(rotation=90)
    plt.show()