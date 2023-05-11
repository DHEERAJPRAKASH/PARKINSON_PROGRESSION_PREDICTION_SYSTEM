from flask import Flask, render_template, request, flash,redirect
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import pickle
from featuresFun import features
from supportFun import loadData,smape

models = pickle.load(open('static/datas/models1.pkl', 'rb'))
mms = MinMaxScaler()
app=Flask(__name__)
app.secret_key="123"

app.config["UPLOAD_FOLDER1"]="static/excel"

@app.route("/home")
def land():
    return render_template("Landing.html")

@app.route("/",methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('file')
        print(files)
        for upload_file in files:
            if upload_file.filename != '':
                file_path = os.path.join(app.config["UPLOAD_FOLDER1"], upload_file.filename)
                upload_file.save(file_path)
                try:
                    df = pd.read_csv(file_path)
                    if df.empty:
                        flash('The uploaded file does not contain any data.')
                        return render_template('Upload.html')
                except pd.errors.ParserError:
                    return render_template('Upload.html')
        return redirect("/getTable")
    return render_template("Upload.html")

@app.route('/getData')
def viewData():

    def map_test(x):
        print("df",df)
        updrs = x.split('_')[2] + '_' + x.split('_')[3]
        month = int(x.split('_plus_')[1].split('_')[0])
        visit_id = x.split('_')[0] + '_' + x.split('_')[1]
        if updrs == 'updrs_3':
            rating = df[df.visit_id == visit_id]['pred2'].values[0]
        elif updrs == 'updrs_4':
            rating = 0
        elif updrs == 'updrs_1':
            rating = df[df.visit_id == visit_id]['pred0'].values[0]
        else:
            rating = df[df.visit_id == visit_id]['pred1'].values[0]
        return rating
    try:
        test = pd.read_csv("static/excel/test.csv")
        test_proteins = pd.read_csv("static/excel/test_proteins.csv")
        test_peptides = pd.read_csv("static/excel/test_peptides.csv")
        sample_submission = pd.read_csv("static/excel/sample_submission.csv")

        df = test[['visit_id']].drop_duplicates('visit_id')
        pred_0 = features(df[['visit_id']], test_proteins, test_peptides, 0)
        scale_col = ['NPX_min', 'NPX_max', 'NPX_mean', 'NPX_std', 'Abe_min', 'Abe_max', 'Abe_mean', 'Abe_std']
        pred_0[scale_col] = mms.fit_transform(pred_0[scale_col])
        pred_0 = (models['rfc_0'].predict(pred_0.drop(columns=['visit_id'], axis=1)) \
                      + models['svc_0'].predict(pred_0.drop(columns=['visit_id'], axis=1)) \
                      + models['linear_0'].predict(pred_0.drop(columns=['visit_id'], axis=1)) \
                      + models['lgbm_0'].predict(pred_0.drop(columns=['visit_id'], axis=1)) \
                      + models['xgb_0'].predict(pred_0.drop(columns=['visit_id'], axis=1))) / 5
        df['pred0'] = np.ceil(pred_0 + 0)

        pred_1 = features(df[['visit_id']], test_proteins, test_peptides, 1)
        scale_col = ['NPX_min', 'NPX_max', 'NPX_mean', 'NPX_std', 'Abe_min', 'Abe_max', 'Abe_mean', 'Abe_std']
        pred_1[scale_col] = mms.fit_transform(pred_1[scale_col])
        pred_1 = (models['rfc_1'].predict(pred_1.drop(columns=['visit_id'], axis=1)) \
                      + models['svc_1'].predict(pred_1.drop(columns=['visit_id'], axis=1)) \
                      + models['linear_1'].predict(pred_1.drop(columns=['visit_id'], axis=1)) \
                      + models['xgb_1'].predict(pred_1.drop(columns=['visit_id'], axis=1)) \
                      + models['lgbm_1'].predict(pred_1.drop(columns=['visit_id'], axis=1))) / 5
        df['pred1'] = np.ceil(pred_1 + 0.5)

        pred_2 = features(df[['visit_id']], test_proteins, test_peptides, 2)
        scale_col = ['NPX_min', 'NPX_max', 'NPX_mean', 'NPX_std', 'Abe_min', 'Abe_max', 'Abe_mean', 'Abe_std']
        pred_2[scale_col] = mms.fit_transform(pred_2[scale_col])
        pred_2 = (models['rfc_2'].predict(pred_2.drop(columns=['visit_id'], axis=1)) \
                      + models['svc_2'].predict(pred_2.drop(columns=['visit_id'], axis=1)) \
                      + models['linear_2'].predict(pred_2.drop(columns=['visit_id'], axis=1)) \
                      + models['xgb_2'].predict(pred_2.drop(columns=['visit_id'], axis=1)) \
                      + models['lgbm_2'].predict(pred_2.drop(columns=['visit_id'], axis=1))) / 5
        df['pred2'] = np.ceil(pred_2 + 1.5)
        sample_submission['rating'] = sample_submission['prediction_id'].apply(map_test)
        message='fill'
        return render_template('Predictor.html', data=sample_submission.to_html(), message=message)
    except:
        message="Any of the Following Dataset is Missing:"
        return render_template('Predictor.html', message=message)

@app.route('/getTable', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        button_clicked = request.form['button']

        if button_clicked == 'Test Data':
            try:
                dat = pd.read_csv('static/excel/test.csv')
                message = dat.to_html()
            except:
                message = """<p>Test Data is Not Yet Loaded</p><br><br> <a href="/">Click Here to Load</a>"""
            return render_template('ViewData.html', message=message, titles="Test Dataset")

        elif button_clicked == 'Protein Data':
            try:
                dat = pd.read_csv('static/excel/test_proteins.csv')
                message = dat.to_html()
            except:
                message = """<p>Protein Data is Not Yet Loaded</p><br><br> <a href="/">Click Here to Load</a>"""
            return render_template('ViewData.html', message=message, titles="Protein Dataset")

        elif button_clicked == 'Peptide Data':
            titles = "Peptide Dataset"
            try:
                dat = pd.read_csv('static/excel/test_peptides.csv')
                message = dat.to_html()
            except:
                message = """<p>Peptide Data is Not Yet Loaded</p><br><br> <a href="/">Click Here to load</a>"""

            return render_template('ViewData.html', message=message, titles=titles)
    return render_template('ViewData.html')
if __name__=='__main__':
    app.run(debug=True)