# Poke DB

A data pipeline that extracts Pokémon data from [PokeAPI](https://pokeapi.co/) 
into structured CSVs for analysis.

## Data Model
| Table | Description |
|---|---|
| fact_pokemon | Core Pokémon attributes |
| dim_moves | Pokémon ↔ move mappings |
| dim_stats | Base stats per Pokémon |
| dim_types | Type assignments |
| dim_abilities | Ability mappings |
| fact_moves | Move details and flavor text |
| fact_abilities | Ability descriptions by version |
| fact_versions | Game version metadata |

## Notes
- Data sourced from PokeAPI (free, no auth required)
- CSVs output to /data directory (excluded from repo)