from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
import uuid
import json
from data.Checklist import Checklist
from data.function import file_writer, file_reader, file_reset
from data.CL_Library import CL_Library

app = Flask(__name__, static_folder='static')

checklistpath = "data/checklists.json"
historypath = "data/history.json"

@app.route("/")
def home():
    return render_template('base.html')

@app.route("/create_interface")
def create_interface():
    return render_template('createinterface.html')

@app.route("/fill_checklist/<checklist_id>")
def fill_checklist(checklist_id):
    registred_checklists = file_reader(checklistpath)  # lit le fichier JSON
    selected = next((cl for cl in registred_checklists if cl['id'] == checklist_id), None)

    if selected is None:
        return f"Checklist {checklist_id} introuvable", 404

    return render_template('fillchecklist.html', checklist=selected)

@app.route("/history")
def history():
    new_checklists = CL_Library([])
    new_checklists = file_reader(historypath)
    return render_template('history.html', new_checklists=new_checklists)

@app.route('/create_checklist', methods=['POST'])
def create_checklist():
    title_cl = request.form['title_cl']
    element1 = request.form['element1']
    element2 = request.form['element2']
    element3 = request.form['element3']
    new_checklist = Checklist(title_cl, element1, element2, element3)
    file_writer(new_checklist,checklistpath)
    return render_template('createstate.html', title_cl=title_cl, element1 = element1, element2 = element2, element3 = element3)

@app.route('/checklist_choice')
def checklist_choice():
    new_checklists = CL_Library([])
    new_checklists = file_reader(checklistpath)
    return render_template('listofchecklist.html', new_checklists=new_checklists)

@app.route('/submit_checklist/<checklist_id>', methods=['POST'])
def submit_checklist(checklist_id):
    checklists = file_reader(checklistpath)

    updated_checklists = []
    completed_checklist = None

    for cl_data in checklists:
        if cl_data["id"] == checklist_id:

            cl_data["tick1"] = 'tick1' in request.form
            cl_data["tick2"] = 'tick2' in request.form
            cl_data["tick3"] = 'tick3' in request.form

            if cl_data["tick1"] and cl_data["tick2"] and cl_data["tick3"]:
                completed_checklist = cl_data
            else:
                updated_checklists.append(cl_data)
        else:
            updated_checklists.append(cl_data)

    if completed_checklist:
        history = file_reader(historypath)
        history.append(completed_checklist)
        file_writer(history, historypath)

    if len(updated_checklists) > 0:
        file_reset(checklistpath)
    file_writer(updated_checklists, checklistpath)
    

    return redirect(url_for('checklist_choice'))



if __name__ == '__main__':
    app.run(debug=True, port=5001)