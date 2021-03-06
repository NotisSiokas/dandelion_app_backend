from flask import render_template, url_for, redirect
from flask_json import json_response
from app.admin import admin
from app.models import Experiment
from app import db
from app.utils.functions import row2dict


@admin.route('/experiment', methods=['GET'])
def listExperiment():
    experiment = Experiment.query.all()

    return json_response(data=(row2dict(x) for x in experiment))



@admin.route('/experiment/add', methods=['GET', 'POST'])
def add_experiment():
    form = ExperimentForm()
    if form.validate_on_submit():
        experiment = Experiment(name=form.name.data)
        try:
            db.session.add(experiment)
            db.session.commit()
        except:
            db.session.rollback()

        return redirect(url_for('admin.list_experiment'))

    return render_template('admin/experiment.html',
                           form=form,
                           title="Add experiment")




    return render_template('admin/experiment.html',
                           form=form,
                           experiment=experiment,
                           title='Edit experiment')


