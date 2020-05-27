import plotly.graph_objects as go
import csv

t=0
f1=0
c=0
with open('clickbaitUserResult.csv') as f:
    data = csv.reader(f)
    for row in data:
        c+=1
        if c>1:
            if float(row[1])>=15:
                t+=1
            else:
                f1+=1

labels = ['True Positive --> '+str(t), 'False Negative --> '+str(f1)]
values = [t,f1]

# Use `hole` to create a donut-like pie chart
fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent', hole=0.3)])
fig.update_layout(
    title_text="Clickbait User profiles",
    )
fig.show()









