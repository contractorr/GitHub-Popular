import requests
from plotly.graph_objs import Bar
from plotly import offline
import re
# Make an API call
url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'
headers = {'Accept': 'application/vnd.github.v3+json'}
r = requests.get(url, headers=headers)
print(f"Status code: {r.status_code}")

# Store the API response
response_dict = r.json()

# Process results:
print(response_dict.keys()) # ['total _count', 'incomplete_results', 'items']
# Print the total number of Python repositories in GitHub
print(f"Total Repositories: {response_dict['total_count']}")
# The value associated with 'items' is a list containing a number of dictionaries, one for each repository returned. Let's store this list in repo_dicts
repo_dicts = response_dict['items']
# Print the length of repo_dicts to find the number of dictionaries, and therefore repositories, we have information for
print(f"Repositories returned: {len(repo_dicts)}")
# Lets store the first dictionary in repo_dict
# repo_dict = repo_dicts[0]
# Lets print all the information we have in this dictionary
# print(f"\nKeys: {len(repo_dict)}")
# for key in sorted(repo_dict.keys()):
#     print(f"\t{key}")

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
