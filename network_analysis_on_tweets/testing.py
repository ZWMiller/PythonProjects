import graph_builder as gb
from cleaning_functions import clean_user_name

degree_test_known_answer = [('Joyce Alene', 10), ('Rob Reiner', 10), ('Rachel Maddow MSNBC', 9),
                             ('Facts Do Matter', 9), ('Daniel Dale', 7), ('Jim Sciutto', 6), ('The White House', 6),
                             ('Bill Mitchell', 5), ("Lawrence O'Donnell", 5), ('David Corn', 5)]

def test_degree_analysis():
    graph = gb.build_graph_from_csvs("test_data/", num_files=None)
    analysis_result = gb.get_hub_nodes(graph, top_n_hubs=10)
    assert analysis_result == degree_test_known_answer, "Degree analysis does not match known solution."
    return 1

def cleaning_test(user_name, correct_value):
    assert str(clean_user_name(user_name)) == str(correct_value), "Cleaning function failed on {}".format(user_name)
    return 1


degree_test_result = test_degree_analysis()

with open('test_data/cleaning_unit_test_data.txt') as f:
    for line in f.readlines():
        raw, correct = line.split(";,.")
        cleaning_test(raw, correct.replace('\n',''))
print("All tests passed.")