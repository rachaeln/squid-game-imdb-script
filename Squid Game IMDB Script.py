import bs4
import pandas as pd
from requests import get

squid_game_info = []

url = 'https://www.imdb.com/title/tt10919420/episodes/?ref_=tt_ep_epl'

response = get(url)

squid_game_html = bs4.BeautifulSoup(response.text, 'html.parser')

episode_containers = squid_game_html.find_all('div', class_='info')

# For loop to get each episode's attributes

for episodes in episode_containers:

    episode_number = episodes.meta['content']
    title = episodes.a['title']
    airdate = episodes.find('div', class_='airdate').text.strip()
    rating = episodes.find('span', class_='ipl-rating-star__rating').text
    total_votes = episodes.find('span', class_='ipl-rating-star__total-votes').text
    description = episodes.find('div', class_='item_description').text.strip()

    episode_info = [episode_number, title, airdate, rating, total_votes, description]

    squid_game_info.append(episode_info)

# Making dataframe with pandas

squid_game_info = pd.DataFrame(squid_game_info, columns = ['episode_number', 'title', 'airdate', 'rating', 'total_votes', 'description'])

# Removing parentheses from total_votes

def remove_par(votes):
    for x in ((',',''), ('(',''),(')','')):
        votes = votes.replace(*x)
        
    return votes

squid_game_info['total_votes'] = squid_game_info.total_votes.apply(remove_par).astype(int)

# Converting rating from a string to a number

squid_game_info['rating'] = squid_game_info.rating.astype(float)

# squid_game_info.to_csv('Squid_Game_IMDB_Info.csv',index=False)