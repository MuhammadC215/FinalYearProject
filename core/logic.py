def match_score(a1, a2):

    #/* ROOT NODE */
    if a1.injury_status or a2.injury_status:
        return 0, "Unsafe - one athlete has an active injury, sparring not recommended."

    weight_diff = abs(a1.weight - a2.weight)
    skill_diff = abs(a1.skill_level - a2.skill_level)
    exp_diff = abs(a1.experience_years - a2.experience_years)

    # LEVEL 1 DECISION
    if weight_diff > 15:
        return 0, "Unsafe - extreme weight difference increases injury risk significantly."

    if skill_diff >= 4 and exp_diff >= 4:
        return 0, "Unsafe - large mismatch in both skill and experience."

    # LEVEL 2 DECISION
    if weight_diff > 8:
        return 1, "Medium risk - noticeable weight difference may affect safety in sparring."

    if skill_diff >= 3:
        return 1, "Medium risk - skill levels are not closely matched."

    if exp_diff >= 3:
        return 1, "Medium risk - experience gap may lead to uneven sparring intensity."

    # LEAF NODE
    return 2, "Safe - both athletes are closely matched across weight, skill, and experience."