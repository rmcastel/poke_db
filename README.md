# Poke DB

A data pipeline that extracts Pokémon data from [PokeAPI](https://pokeapi.co/) 
into structured CSVs as well as a .db file for analysis.

## Inspiration
In late 2022 I had my first interaction with the data engineering process, working alongside a data engineer on my team. Thought the experience, I saw the importance of data engineering and found it to be fun. I wanted more practice with data engineering (as well as with working with APIs in general) and came across the PokeAPI. The following code is a python data engineering pipeline that calls the PokeAPI and creates a database (.db filetype) that tries to follow the [STAR schema](https://en.wikipedia.org/wiki/Star_schema).


The API itself is quite rich, but I only pulled in data that I found relevant or interesting. For example, we have an option of pulling the flavor text for every game and every language said game has been released in. Ultimately, only the English flavor text was brought in, but it is possible to bring in the English, Spanish, and Japanese flavor text if desired. The API is free but enforces rate limits on excessive calls. I tried to account for API call limits in the code, but a user may still run into rate limit errors.

## Data Model
| Table | Description |
|---|---|
| fact_pokemon | Core Pokémon attributes |
| dim_moves | Pokémon ↔ move mappings |
| dim_stats | Base stats per Pokémon |
| dim_types | Type assignments |
| dim_abilities | Ability mappings |
| fact_moves | Move details and flavor text (en)|
| fact_abilities | Ability descriptions by version |
| fact_versions | Game version metadata |

## Folder Structure
```bash
.
├── data
│   ├── dim_abilities
│   │   └── dim_abilities_yyyymmdd.csv
│   ├── dim_games
│   │   └── dim_games_yyyymmdd.csv
│   ├── dim_moves
│   │   └── dim_moves_yyyymmdd.csv
│   ├── dim_stats
│   │   └── dim_stats_yyyymmdd.csv
│   ├── dim_types
│   │   └── dim_types_yyyymmdd.csv
│   ├── fact_abilities
│   │   └── fact_abilities_yyyymmdd.csv
│   ├── fact_moves
│   │   └── fact_moves_yyyymmdd.csv
│   ├── fact_pokemon
│   │   └── fact_pokemon_yyyymmdd.csv
│   └── fact_versions
│       └── fact_versions_yyyymmdd.csv
├── ex.sql
├── get_poke.py
├── make_db.py
├── pokemon.db
└── README.md
```

## Notes
- Data sourced from PokeAPI (free, no auth required)
- CSVs output to /data directory (excluded from repo because sizing concerns)