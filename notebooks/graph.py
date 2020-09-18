import plotly.graph_objects as go
import pandas as pd

#url = "https://github.com/mustajabakhtar/manha/blob/master/data_set.csv"
dataset = pd.read_csv('../data/graph.csv')
#dataset = pd.read_csv(url)

days = ["17", "16", "15", "14", "13", "12", "11", "10", "09", "08", "07"]

# make list of cities
cities = []
for city in dataset["city"]:
    if city not in cities:
        cities.append(city)
# make figure
fig_dict = {
    "data": [],
    "layout": {},
    "frames": []
}

# fill in most of layout
fig_dict["layout"]["xaxis"] = {"range": [30, 85], "title": "Beaten"}
fig_dict["layout"]["yaxis"] = {"title": "Meet", "type": "log"}
fig_dict["layout"]["hovermode"] = "closest"
fig_dict["layout"]["updatemenus"] = [
    {
        "buttons": [
            {
                "args": [None, {"frame": {"duration": 500, "redraw": False},
                                "fromcurrent": True, "transition": {"duration": 300,
                                                                    "easing": "quadratic-in-out"}}],
                "label": "Play",
                "method": "animate"
            },
            {
                "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                  "mode": "immediate",
                                  "transition": {"duration": 0}}],
                "label": "Pause",
                "method": "animate"
            }
        ],
        "direction": "left",
        "pad": {"r": 10, "t": 87},
        "showactive": False,
        "type": "buttons",
        "x": 0.1,
        "xanchor": "right",
        "y": 0,
        "yanchor": "top"
    }
]

sliders_dict = {
    "active": 0,
    "yanchor": "top",
    "xanchor": "left",
    "currentvalue": {
        "font": {"size": 20},
        "prefix": "Date:",
        "visible": True,
        "xanchor": "right"
    },
    "transition": {"duration": 300, "easing": "cubic-in-out"},
    "pad": {"b": 10, "t": 50},
    "len": 0.9,
    "x": 0.1,
    "y": 0,
    "steps": []
}

# make data
day = 7
for city in cities:
    dataset_by_day = dataset[dataset["day"] == day]
    dataset_by_day_and_cont = dataset_by_day[
        dataset_by_day["city"] == city]

    data_dict = {
        "x": list(dataset_by_day_and_cont["beaten"]),
        "y": list(dataset_by_day_and_cont["total"]),
        "mode": "markers",
        "text": list(dataset_by_day_and_cont["vendor"]),
        "marker": {
            "sizemode": "area",
            "sizeref": 200,
            "size": list(dataset_by_day_and_cont["hotels"])
        },
        "name": city
    }
    fig_dict["data"].append(data_dict)

# make frames
for day in days:
    frame = {"data": [], "name": str(day)}
    for city in cities:
        dataset_by_day = dataset[dataset["day"] == int(day)]
        dataset_by_day_and_cont = dataset_by_day[
            dataset_by_day["city"] == city]

        data_dict = {
            "x": list(dataset_by_day_and_cont["beaten"]),
            "y": list(dataset_by_day_and_cont["total"]),
            "mode": "markers",
            "text": list(dataset_by_day_and_cont["vendor"]),
            "marker": {
                "sizemode": "area",
                "sizeref": 200,
                "size": list(dataset_by_day_and_cont["hotels"])
            },
            "name": city
        }
        frame["data"].append(data_dict)

    fig_dict["frames"].append(frame)
    slider_step = {"args": [
        [day],
        {"frame": {"duration": 300, "redraw": False},
         "mode": "immediate",
         "transition": {"duration": 300}}
    ],
        "label": day,
        "method": "animate"}
    sliders_dict["steps"].append(slider_step)

fig_dict["layout"]["sliders"] = [sliders_dict]

fig = go.Figure(fig_dict)

fig.show()
