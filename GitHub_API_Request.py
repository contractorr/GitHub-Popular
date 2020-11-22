import requests
from plotly.graph_objs import Bar
from plotly import offline

# Make an API call to GitHub
url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'
headers = {'Accept': 'application/vnd.github.v3+json'}
r = requests.get(url, headers=headers)
print(f"Status code: {r.status_code}")

# Store the API response
response_dict = r.json()

# Process results
# The value associated with 'items' is a list containing a number of dictionaries, one for each repository returned. Let's store this list in repo_dicts
repo_dicts = response_dict['items']


repo_links, stars, tooltips = [], [], []
for repo_dict in repo_dicts:
    repo_name = repo_dict['name']
    repo_url = repo_dict['html_url']
    stars.append(repo_dict['stargazers_count'])
    owner = repo_dict['owner']['login']
    desc = repo_dict['description']
    # Plotly allows you to use HTML code within text elements, so we can generate a string for the label with a line break (<br />) and add links to our x labels
    repo_link = f"<a href='{repo_url}'>{repo_name}</a>"
    repo_links.append(repo_link)
    label = f"{owner}<br />{desc}"
    tooltips.append(label)

# Make chart
data = [{
    'type': 'bar',
    'x': repo_links,
    'y': stars,
    'hovertext': tooltips,
    'marker': {
        'color': 'rgb(60, 100, 150)',
        'line': {'width': 1.5, 'color': 'rgb(25, 25, 25)'},
        'opacity': 0.6
    }
}]

my_layout = {
    'title': 'Most-Starred Python Projects on GitHub',
    'titlefont': {'size': 28},
    'xaxis': {
        'title': 'Repository',
        'titlefont': {'size': 24},
        'tickfont': {'size':14}
    },
    'yaxis': {
        'title': 'Stars',
        'titlefont': {'size': 24},
        'tickfont': {'size': 14}
    },
}

fig = {'data': data, 'layout': my_layout}
offline.plot(fig, filename='python_repos.html')
