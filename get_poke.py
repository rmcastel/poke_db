#https://pokeapi.co/docs/v2#pokemon
import requests
import os
import csv
import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time


# prevent timing out
session = requests.Session()
retry = Retry(
    connect=3,
    read=3,           # retries on read timeouts
    backoff_factor=1, # wait 1s, 2s, 4s between retries
    status_forcelist=[429, 500, 502, 503, 504],  # retry on these HTTP codes
    raise_on_status=False
)
adapter = HTTPAdapter(max_retries=retry)
session.mount('https://', adapter)
today=datetime.datetime.today()
today_str=today.strftime(f'%Y%m%d')
month=today.strftime(f'%Y%m')
year=today.strftime(f'%Y')
wd=os.getcwd()


base_url=fr'https://pokeapi.co/api/v2/pokemon/'
base_ability_url=fr'https://pokeapi.co/api/v2/ability/'
base_moves_url=fr'https://pokeapi.co/api/v2/move/'
base_version_url=fr'https://pokeapi.co/api/v2/version/'
total_pokemons=requests.get(url=base_url).json()['count']
total_abilities=requests.get(url=base_ability_url).json()['count']
total_moves=requests.get(url=base_moves_url).json()['count']
total_versions=requests.get(url=base_version_url).json()['count']

def safe_get(url, retries=3):
    for attempt in range(retries):
        try:
            response = session.get(url, timeout=10)  # ← uses session here
            if response.status_code == 429:
                wait = int(response.headers.get('Retry-After', 60))
                print(f"Rate limited. Waiting {wait}s...")
                time.sleep(wait)
                continue
            return response
        except requests.exceptions.ReadTimeout:
            print(f"Timeout on {url}, attempt {attempt+1}")
            time.sleep(2 ** attempt)
    return None

#function to make file structure
def make_directory(path):
    if not os.path.exists(path=path):
        try:
            os.makedirs(path)
            print(f'Created: {path}')
        except ValueError as err:
            print(err.args)
    else:
        print(f'Path {path} exists')


def append_to(lst, col, replace_value=False):
    try:
        lst.append(col)
    except:
        lst.append(replace_value)


def clean_text(text):
    text = text.replace('\n', ' ')
    return " ".join(text.split())


poke_facts=[]
poke_stats=[]
poke_types=[]
poke_abilities=[]
poke_moves=[]
poke_games=[]
abilities_facts=[]
moves_facts=[]
version_facts=[]

code_break = 0
print(f"Total Version: {total_versions}")
for version_id in range(total_versions + 1): # total_versions
    version_url=base_version_url+str(version_id)
    # version_data=requests.get(version_url)
    version_data = safe_get(version_url)
    if version_data is None or version_data.status_code!=200:
        print(version_url)
        print(f"Version Break: {version_id}")
        code_break+=1
        continue
    else:
        version_data=version_data.json()
    
    if code_break>20:
        break

    id = version_data['id']
    name = version_data['name']
    print(name, version_id)
    version_group = version_data['version_group']['name']

    version_groups = requests.get(url=version_data['version_group']['url']).json()
    generation = version_groups['generation']['name']

    for region in version_groups['regions']:
        region_name = region['name']

        row = [
            id,
            name,
            version_group,
            generation,
            region_name,
        ]
        version_facts.append(row)

code_break = 0
print(f"Total Moves: {total_moves}")
for move_id in range(total_moves + 1):
    move_url=base_moves_url+str(move_id)
    # move_data=requests.get(move_url)
    move_data=safe_get(move_url)
    if move_data is None or move_data.status_code!=200:
        print(move_url)
        print(f"Move Break: {move_id}")
        code_break+=1
        continue
    else:
        move_data=move_data.json()
    
    if code_break>20:
        break

    name = move_data['name']
    print(name, move_id)
    move_type = move_data['type']['name']
    pp = move_data['pp']
    priority = move_data['priority']
    accuracy = move_data['accuracy']
    effect_chance = move_data['effect_chance']
    if move_data['contest_type']:
        contest_type = move_data['contest_type']['name']
    else:
        contest_type = False
    damage_class = move_data['damage_class']['name']
    target = move_data['target']['name']
    power = move_data['power']
    if move_data['meta']:
        crit_rate = move_data['meta']['crit_rate']
        drain = move_data['meta']['drain']
        healing = move_data['meta']['healing']
        max_hits = move_data['meta']['max_hits']
        max_turns = move_data['meta']['max_turns']
        min_hits = move_data['meta']['min_hits']
        min_turns = move_data['meta']['min_turns']
        stat_chance = move_data['meta']['stat_chance']
    else:
        crit_rate = False
        drain = False
        healing = False
        max_hits = False
        max_turns = False
        min_hits = False
        min_turns = False
        stat_chance = False

    # Filter for English entries once
    en_entries = [
        (entry['version_group']['name'], entry['flavor_text']) for entry in move_data['flavor_text_entries'] if entry['language']['name'] == 'en'
    ]

    for version, text in en_entries:
        row = [
            name,
            move_type,
            pp,
            priority,
            accuracy,
            effect_chance,
            contest_type,
            damage_class,
            target,
            power,
            crit_rate,
            drain,
            healing,
            max_hits,
            max_turns,
            min_hits,
            min_turns,
            stat_chance,
            clean_text(text), 
            version,
        ]
            
        moves_facts.append(row)

code_break = 0
print(f"Total Abilities: {total_abilities}")
for ability_id in range(total_abilities + 1): # total_abilities
    ability_url=base_ability_url+str(ability_id)
    # ability_data=requests.get(ability_url)
    ability_data=safe_get(ability_url)
    if ability_data is None or ability_data.status_code!=200:
        print(ability_url)
        print(f"Ability Break: {ability_id}")
        code_break+=1
        continue
    else:
        ability_data=ability_data.json()
    
    if code_break>20:
        break

    name = ability_data['name']
    print(name, ability_id)
    is_main = ability_data['is_main_series']
    real_id = ability_data['id']

    # Filter for English entries once
    en_entries = [
        (entry['version_group']['name'], entry['flavor_text']) for entry in ability_data['flavor_text_entries'] if entry['language']['name'] == 'en'
    ]

    for version, text in en_entries:
        row = [
            name, 
            real_id, 
            is_main, 
            clean_text(text), 
            version
        ]
        abilities_facts.append(row)
    
code_break=0
print(f"Total Pokemon: {total_pokemons}")   
for i in range(total_pokemons + 1): # total_pokemons
    pokemon_url=base_url+str(i)
    # poke_fact=requests.get(pokemon_url)
    poke_fact=safe_get(pokemon_url)
    if poke_fact is None or poke_fact.status_code!=200:
        print(pokemon_url)
        print(f"Poke Code Break: {i}")
        code_break+=1
        continue
    else:
        poke_fact=poke_fact.json()
        code_break=0
    
    if code_break>20:
        print(f"Poke Code Break!")
        break
    
    #dim_facts
    facts=[]
    print(poke_fact['name'], i)
    facts.append(poke_fact['name'])
    facts.append(poke_fact['id'])
    facts.append(poke_fact['base_experience'])
    facts.append(poke_fact['height'])
    facts.append(poke_fact['is_default'])
    facts.append(poke_fact['order'])
    facts.append(poke_fact['weight'])
    facts.append(len(poke_fact['forms']))
    facts.append(len(poke_fact['game_indices']))
    
    #get evolution
    poke_evol=requests.get(fr'https://pokeapi.co/api/v2/pokemon-species/{i}/').json()
    if isinstance(poke_evol['evolves_from_species'], dict):
        facts.append(poke_evol['evolves_from_species']['name'])
        facts.append(poke_evol['base_happiness'])
        facts.append(poke_evol['capture_rate'])
        facts.append(poke_evol['growth_rate']['name'])
        try:
            append_to(facts, poke_evol['shape']['name'])
        except:
            facts.append(False)
        
        try:
            append_to(facts, poke_evol['habitat']['name'])
        except:
            facts.append(False)
    else:
        facts.append(False)
        facts.append(poke_evol['base_happiness'])
        facts.append(poke_evol['capture_rate'])
        facts.append(poke_evol['growth_rate']['name'])
        try:
            append_to(facts, poke_evol['shape']['name'])
        except:
            facts.append(False)
        
        try:
            append_to(facts, poke_evol['habitat']['name'])
        except:
            facts.append(False)
        
    poke_facts.append(facts)
    
    #dim_stats
    for stat in poke_fact['stats']:
        stats=[]
        stats.append(poke_fact['name'])
        stats.append(poke_fact['id'])
        stats.append(stat['stat']['name'])
        stats.append(stat['base_stat'])
        stats.append(stat['effort'])
        poke_stats.append(stats)
    
    #dim_types
    for type in poke_fact['types']:
        types=[]
        types.append(poke_fact['name'])
        types.append(poke_fact['id'])
        types.append(type['type']['name'])
        types.append(type['slot'])
        poke_types.append(types)
    
    #dim_abilities
    for abil in poke_fact['abilities']:
        abilities=[]
        abilities.append(poke_fact['name'])
        abilities.append(poke_fact['id'])
        abilities.append(abil['ability']['name'])
        abilities.append(abil['is_hidden'])
        abilities.append(abil['slot'])
        poke_abilities.append(abilities)
    
    #dim_moves
    for move in poke_fact['moves']:
        poke= poke_fact['name']
        poke_id = poke_fact['id']
        move_name = move['move']['name']
        move_id = int(move['move']['url'].split('/')[-2])
        move_group_details = [
            (entry['level_learned_at'], entry['move_learn_method']['name'],
             entry['version_group']['name'], ) for entry in move['version_group_details']
        ]
        for level_learn, method, version in move_group_details:
            row = [
                poke,
                poke_id,
                move_name,
                move_id,
                level_learn,
                method,
                version,
            ]
            poke_moves.append(row)
    
    #dim_games
    for game in poke_fact['game_indices']:
        games=[]
        games.append(poke_fact['name'])
        games.append(poke_fact['id'])
        games.append(game['game_index'])
        games.append(game['version']['name'])
        poke_games.append(games)


table_dict={
    'fact_pokemon':[[
        'name',
        'id',
        'base_experience',
        'height',
        'is_default',
        'order',
        'weight',
        'forms',
        'game_indices',
        'evolves_from_species',
        'base_happiness',
        'capture_rate',
        'growth_rate',
        'shape',
        'habitat',
    ], poke_facts],
    'dim_stats':[[
        'name',
        'id',
        'stat',
        'base_stat',
        'effort',
    ], poke_stats],
    'dim_types':[[
        'name',
        'id',
        'type',
        'slot',
    ], poke_types],
    'dim_abilities':[[
        'name',
        'id',
        'ability',
        'is_hidden',
        'slot',
    ], poke_abilities],
    'dim_moves':[[
        'name',
        'id',
        'move',
        'move_id',
        'level_learned_at',
        'move_learn_method',
        'version_group',
    ], poke_moves],
    'dim_games':[[
        'name',
        'id',
        'game_index',
        'version',
    ], poke_games],
    'fact_abilities': [[
        'name',
        'id',
        'is_main_series',
        'text',
        'version',
    ], abilities_facts],
    'fact_moves': [[
        'name',
        'move_type',
        'pp',
        'priority',
        'accuracy',
        'effect_chance',
        'contest_type',
        'damage_class',
        'target',
        'power',
        'crit_rate',
        'drain',
        'healing',
        'max_hits',
        'max_turns',
        'min_hits',
        'min_turns',
        'stat_chance',
        'text',
        'version',
    ], moves_facts],
    'fact_versions': [[
        'id',
        'name',
        'version_group',
        'generation',
        'region_name',
    ], version_facts],
}

for i in table_dict:
    print(i)
    make_directory(f'{wd}/data/{i}') # data/raw/{year}/{month}
    file_name=f'{wd}/data/{i}'+f'/{i}_{today_str}.csv'
    with open(file_name, 'w', newline='', encoding='utf-8') as out:
        writer = csv.writer(out, quoting=csv.QUOTE_MINIMAL)
        writer.writerow( table_dict[i][0] )
    
        for row in table_dict[i][-1]:
            writer.writerow(row)    
