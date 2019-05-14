from model.project import get_all_project_positions_by_id
test_id = 1

positions = get_all_project_positions_by_id(test_id)

for p in positions:
    print(p)