from parse_query import Parse
import os
import json
from flask import Flask, jsonify, request, Blueprint, render_template, abort, send_from_directory
from jinja2 import TemplateNotFound
from qt2vis import parse
from input_recommendation_engine import genQSents
from ER_engine import user_recommend,user_recommend_v1
# Import our Example Applications
from server.applications.datatone import datatone_routes
# Initialize the app
app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
java_path = "C:/Program Files/Java/jdk1.8.0_191/bin/java.exe"
os.environ['JAVAHOME'] = java_path
# Initialize parse variable
parse_instance = None
TTM=[]
@app.route('/init', methods=['POST'])
def init():
    global parse_instance
    global TTM
    TTM = [[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2],
           [0.16, 0.12, 0.18, 0.07, 0.12, 0.1, 0.1, 0.12, 0.13],
           [0.1, 0.2, 0.1, 0.1, 0.1, 0.11, 0.09, 0.1, 0.1],
           [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2],
           [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2],
           [0.16, 0.12, 0.18, 0.07, 0.12, 0.1, 0.1, 0.12, 0.13],
           [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2],
           [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2],
           [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2]]
    if parse_instance is not None:
        return jsonify({"message":"parse already initialized"})
    # dependency_parser_config = {'name': 'corenlp','model': os.path.join("assets","jars","stanford-parser-4.0.0-models.jar"),'parser': os.path.join("assets","jars","stanford-parser.jar")}
    parse_instance = Parse(verbose=True)
    return jsonify({"message":"NL4DV Initialized"})
@app.route('/vis', methods=['POST'])
def vis():
    global parse_instance
    global TTM
    if parse_instance is None:
        return jsonify({"message":"parse NOT initialized"})
    query = request.form['query']
    table_path=request.form['table_path']
    table_path='./assets/data/'+table_path
    feedback=request.form['Feedback']
    print(feedback)
    print(query)
    print(table_path)
    query_history=parse(query,table_path)
    option=query_history.get("option")
    attributes=query_history.get("attributes")
    task=query_history.get("task")
    # recommend=user_recommend(attributes,task,table_path,feedback)
    recommend,TTM=user_recommend_v1(attributes,task,table_path,feedback,TTM)
    result={"option":option,"recommend":recommend,"task":task}
    return json.dumps(result)
@app.route('/input_association', methods=['POST'])
def Input_association():
    global parse_instance
    if parse_instance is None:
        return jsonify({"message":"parse NOT initialized"})
    query = request.form['Querysent']
    table_path=request.form['Dataset']
    table_path='./assets/data/'+table_path
    print(query)
    print(table_path)
    data=genQSents(query,table_path)
    # data=["1","2"]
    res={"association":data}
    print(json.dumps(res))
    return json.dumps(res)

@app.route('/setDependencyParser', methods=['POST'])
def setDependencyParser():
    global parse_instance
    if parse_instance is None:
        return jsonify({"message":"parse NOT initialized"})
    dependency_parser_config = {'name': 'corenlp','model': os.path.join("assets","jars","stanford-parser-4.0.0-models.jar"),'parser': os.path.join("assets","jars","stanford-parser.jar")}
    parse_instance.set_dependency_parser(config=dependency_parser_config)


@app.route('/setData', methods=['POST'])
def setData():
    global parse_instance
    if parse_instance is None:
        return jsonify({"message":"parse NOT initialized"})

    dataset = request.form['dataset']
    if dataset is not None:
        datafile_obj = dataset.rsplit(".")
        parse_instance.data_genie_instance.set_data(data_url=os.path.join("assets", "data", datafile_obj[0] + ".csv"))
        parse_instance.data_genie_instance.set_alias_map(alias_url=os.path.join("assets", "aliases", datafile_obj[0] + ".json"))
        print(get_dataset_meta())
        return get_dataset_meta()
    else:
        raise ValueError('Data not provided')

@app.route('/setIgnoreList', methods=['POST'])
def setIgnoreList():
    global parse_instance
    if parse_instance is None:
        return jsonify({"message":"parse NOT initialized"})

    ignore_words = request.form['ignore_words']
    parse_instance.data_genie_instance.set_ignore_words(ignore_words=json.loads(ignore_words))
    return jsonify({'message': 'Ignore List Set successfully'})


@app.route('/setThresholds', methods=['POST'])
def setThresholds():
    global parse_instance
    if parse_instance is None:
        return jsonify({"message":"parse NOT initialized"})

    thresholds_str = request.form['thresholds']
    try:
        thresholds = json.loads(thresholds_str)
        response = parse_instance.set_thresholds(thresholds)
        return jsonify({'message': 'Thresholds Set successfully'})
    except:
        raise ValueError('Thresholds not a JSON string')


@app.route('/setImportanceScores', methods=['POST'])
def setImportanceScores():
    global parse_instance
    if parse_instance is None:
        return jsonify({"message":"parse NOT initialized"})

    scores_str = request.form['importance_scores']
    try:
        scores = json.loads(scores_str)
        response = parse_instance.set_importance_scores(scores)
        return jsonify({'message': 'Scores Set successfully'})

    except Exception:
        raise ValueError('Importance Scores not a JSON string')


@app.route('/analyze_query', methods=['POST'])
def analyze_query():
    global parse_instance
    if parse_instance is None:
        return jsonify({"message":"parse NOT initialized"})

    query = request.form['query']
    return json.dumps(parse_instance.analyze_query(query, debug=True))


@app.route('/setAttributeDataType', methods=['POST'])
def setAttributeDataType():
    global parse_instance
    if parse_instance is None:
        print("parse is null")
        return jsonify({"message":"parse NOT initialized"})

    attr_type_obj = request.form['attr_type_obj']
    parse_instance.data_genie_instance.set_attribute_datatype(json.loads(attr_type_obj))
    return get_dataset_meta()


@app.route('/',methods=['GET'])
def application_homepage():
    try:
        return render_template('datatone.html')
    except TemplateNotFound:
        abort(404)


def get_dataset_meta():
    global parse_instance
    output = {
        "summary": parse_instance.data_genie_instance.data_attribute_map,
        "rowCount": parse_instance.data_genie_instance.rows,
        "columnCount": len(parse_instance.data_genie_instance.data_attribute_map.keys())
    }
    return jsonify(output)

if __name__ == "__main__":
    app.register_blueprint(datatone_routes.datatone_bp, url_prefix='/datatone')
    app.run(host='0.0.0.0', debug=True, threaded=True, port=7001)
