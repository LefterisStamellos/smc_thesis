from flask import Flask,request,render_template,jsonify
from wautilpack import Loader,DrumSounds
from flask.ext.cors import CORS
from random import sample

app = Flask(__name__)
CORS(app)


DIRS = {
'model_dir': 'static/kNN_real_set_12FEATS_nosil',
'alt_pardir': 'static/chosen_alt_sounds',
}

FILENAMES = {
'alt_names': 'alt_test_names_with_unspecified.csv',
'model_pkl': 'kNN_real_set.pkl',
'alt_feats': 'alt_set_with_unspecified_12feats.csv',
}

#create Loader instance to load all necessary "preparatory" files
loader = Loader(DIRS,FILENAMES)

#create DrumSounds to load actual sounds, after loading its parameters
model = loader.load_model()
alt_sounds_filenames = loader.load_alt_sounds_filenames()
X = loader.load_alt_sounds_feat_values()
drums = DrumSounds(X,model,alt_sounds_filenames)
loop = ['kick','snare','hihat','crash','ride','rim','tom']


@app.route('/',methods=["GET"])
def index():
	return render_template('index.html')

@app.route('/experiment/',methods=["GET"])
def experiment():
	return render_template('experiment.html')

@app.route('/random/',methods=["GET", "POST"])
def loop_exp(loader = loader,drums = drums,loop = loop):
	alt_inst_loop = {}
	for inst in loop:
		alt_inst_loop[inst] = 'http://localhost:5000/static/alt_sounds/'+drums.one_alt(inst)
	return jsonify(**alt_inst_loop)

@app.route('/stepsorder/',methods=["GET"])
def stepsorder():
	steps = {}
	steps_list =  sample(xrange(3,22), 19)
	steps_list = [str(i) for i in steps_list]
	for s in range(len(steps_list)):
		steps[str(s)] = steps_list[s]
	return jsonify(**steps)

@app.route('/finalize/',methods=["POST","GET"])
def finalize():
    answers = request.json
    df = loader.dump_answers_to_json(answers)
    df.to_json('answers.json')
    return answers

if __name__ == '__main__':
	app.run(host = '0.0.0.0',debug = True)
    # app.run(host = 'http://lefterisstamellos.pythonanywhere.com',debug = True)
