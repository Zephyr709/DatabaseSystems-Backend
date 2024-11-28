CREATE or REPLACE VIEW meal_log_view AS
SELECT 
    d.meallogid,
    d.userid,
    d.fooditemid,
    datelogged,
    f.name,
    f.calories,
    f.protein,
    f.carbs,
    f.fats,
    f.fiber,
    f.sugar,
    f.sodium,
    f.cholesterol
FROM dailymeallog d
JOIN fooditem f
ON d.fooditemid = f.fooditemid;

