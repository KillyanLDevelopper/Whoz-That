SELECT perso.perso_id,color_name, style_name, perso_name, gender_name,  species_name, birthday, personality_name, phrase_name, song_name, hobby_name, quote, cloth_name, skill_name, goal_name, fear_name, siblings_name, coffee_beans_name, coffee_milk_name, coffee_sugar_name FROM perso 
JOIN rel_perso_style ON perso.perso_id = rel_perso_style.perso_id
JOIN styles ON styles.style_id = rel_perso_style.style_id
JOIN rel_perso_color ON perso.perso_id = rel_perso_color.perso_id 
JOIN colors ON colors.color_id = rel_perso_color.color_id
JOIN gender ON gender.gender_id=perso.gender_id
JOIN species ON species.species_id=perso.species_id
JOIN personality ON personality.personality_id=perso.personality_id
JOIN phrase ON phrase.phrase_id=perso.phrase_id
JOIN song ON song.song_id=perso.song_id
JOIN hobby ON hobby.hobby_id=perso.hobby_id
JOIN clothes ON clothes.cloth_id=perso.cloth_id
JOIN skill ON skill.skill_id=perso.skill_id
JOIN goal ON goal.goal_id=perso.goal_id
JOIN fear ON fear.fear_id=perso.fear_id
JOIN siblings ON siblings.siblings_id=perso.siblings_id
JOIN coffee_beans ON coffee_beans.coffee_beans_id=perso.coffee_beans_id
JOIN coffee_milk ON coffee_milk.coffee_milk_id=perso.coffee_milk_id
JOIN coffee_sugar ON coffee_sugar.coffee_sugar_id=perso.coffee_sugar_id;