from flask import Flask, render_template, request
import csv
import io
from fairpy_git.fairpy.fairpy import*
from fairpy_git.fairpy.fairpy.items import course_allocation_by_proxy_auction as ca

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    input_file = request.files['input_file']
    if not input_file:
        return "No file uploaded"

    input_file.seek(0)
    reader = csv.DictReader(io.TextIOWrapper(input_file))
    agent_list_from_csv = []
    course_list = []
    course_capacity = None
    course_amount_per_agent = None
    for row in reader:
        field_names = list(row.keys())
        field_values = row.values()
        data = dict(zip(field_names, field_values))
        if not course_list:
            course_list=list(row.keys())
            course_list.remove('Name')
            course_list.remove('course_capacity')
            course_list.remove('course_amount_per_agent')
        if not course_capacity:
            course_capacity = int(row['course_capacity'])
        if not course_amount_per_agent:
            course_amount_per_agent = int(row['course_amount_per_agent'])
        agent_list_from_csv.append(data)
    agent_list = []
    for idx,agent in enumerate(agent_list_from_csv):
        agent_list.append(AdditiveAgent({key:int(agent_list_from_csv[idx][key]) for key in course_list}, name=agent_list_from_csv[idx]['Name']))
    ans = ca.course_allocation(agents=agent_list,course_capacity=course_capacity,course_list=course_list,course_amount_per_agent=course_amount_per_agent)
    return str(ans)
if __name__ == '__main__':
    app.run()
