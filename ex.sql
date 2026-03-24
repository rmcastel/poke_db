SELECT pk.*
      ,fm.name as move_name
      ,fm.power
      ,fm.accuracy
FROM   pokemon.fact_pokemon pk
JOIN   pokemon.dim_moves mv
ON     pk.id = mv.id
AND    mv.version_group = 'diamond-pearl'
JOIN   pokemon.fact_moves fm
ON     mv.move = fm.name
AND    fm.version = 'diamond-pearl'