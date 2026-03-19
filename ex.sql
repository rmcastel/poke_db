SELECT *
FROM   pokemon.fact_pokemon pk
JOIN   (
       SELECT *
       FROM   pokemon.dim_moves
       WHERE  version_group = 'diamond-pearl'
       ) mv
on     pk.id = mv.id
;