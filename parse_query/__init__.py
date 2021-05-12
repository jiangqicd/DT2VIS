# In-built Libraries
import os
import time
from collections import OrderedDict

# Third-Party Libraries
import spacy
from nltk.stem.porter import PorterStemmer
from nltk.parse.stanford import StanfordDependencyParser
from nltk.parse.corenlp import CoreNLPDependencyParser


from parse_query.datagenie import DataGenie
from parse_query.querygenie import QueryGenie
from parse_query.attributegenie import AttributeGenie
from parse_query.taskgenie import TaskGenie
from parse_query.utils import helpers, constants, error_codes
os.environ['STANFORD_PARSER'] = 'E:/stanford-parser-4.0.0/stanford-parser-4.0.0/stanford-parser.jar'
os.environ['STANFORD_MODELS'] ='E:/stanford-parser-4.0.0/stanford-parser-4.0.0/stanford-parser-4.0.0-models.jar'
java_path = "C:/Program Files/Java/jdk1.8.0_191/bin/java.exe"
os.environ['JAVAHOME'] = java_path
class Parse:
    """
    Class exposed to users to interact with the package. Exposes modules in the package via
    public methods

    """

    def __init__(self, data_url=None,
                 alias_url=None,
                 alias_map=None,
                 label_attribute=None,
                 ignore_words=list(),
                 reserve_words=list(),
                 verbose=False):

        # inputs
        self.data_url = data_url
        self.alias_url = alias_url
        self.alias_map = alias_map
        self.label_attribute = label_attribute
        self.ignore_words = ignore_words
        self.reserve_words = reserve_words
        self.verbose = verbose

        # outputs
        self.query_raw = None
        self.query_processed = ""
        self.query_tokens = list()
        self.query_ngrams = dict()
        self.extracted_vis_type = None
        self.extracted_vis_token = None
        self.extracted_tasks = OrderedDict()
        self.extracted_attributes = OrderedDict()
        self.vis_list = None
        self.dependencies = list()

        # Load constants: thresholds, mappings, scores
        self.vis_keyword_map = constants.vis_keyword_map
        self.task_keyword_map = constants.task_keyword_map
        self.match_scores = constants.match_scores
        self.match_thresholds = constants.match_thresholds

        # Others
        self.dialog = False
        self.debug = False

        # initialize porter stemmer instance
        self.porter_stemmer_instance = PorterStemmer()

        # Set the dependency parser
        self.dependency_parser = "corenlp"
        self.dependency_parser_instance = StanfordDependencyParser(path_to_models_jar="E:/stanford-parser-4.0.0/stanford-parser-4.0.0/stanford-parser-4.0.0-models.jar",
                                                                           encoding='utf8')
        # self.set_dependency_parser(dependency_parser_config)

        # Internal Class Instances
        self.data_genie_instance = DataGenie(self)  # initialize a DataGenie instance.
        self.query_genie_instance = QueryGenie(self)  # initialize a QueryGenie instance.
        self.attribute_genie_instance = AttributeGenie(self,data_url=self.data_url)   # initialize a AttributeGenie instance.
        self.task_genie_instance = TaskGenie(self,data_url=self.data_url)  # initialize a TaskGenie instance.


    # ToDo:- Discuss support for non-ascii characters? Fallback from unicode to ascii good enough?
    # ToDo:- Discuss ERROR Handling
    # ToDo:- Utilities to perform unit conversion (eg. seconds > minutes). Problem: Tedious to infer base unit from data. - LATER
    def analyze_query(self, query_raw, dialog=False, debug=False):
        # type: (str) -> dict

        self.dialog = dialog
        self.debug = debug

        # If not a follow-up query, reset the output variables.
        if not dialog:
            self.extracted_tasks = OrderedDict()
            self.extracted_attributes = OrderedDict()

        # CLEAN AND PROCESS QUERY
        self.query_raw = query_raw
        helpers.cond_print("Raw Query: " + self.query_raw, self.verbose)
        self.query_processed = self.query_genie_instance.process_query(self.query_raw)
        self.query_tokens = self.query_genie_instance.clean_query_and_get_query_tokens(self.query_processed, self.reserve_words, self.ignore_words)
        self.query_ngrams = self.query_genie_instance.get_query_ngrams(' '.join(self.query_tokens))
        self.dependencies = self.query_genie_instance.create_dependency_tree(self.query_processed)
        helpers.cond_print("Processed Query: " + self.query_processed, self.verbose)
        # print("tokens:")
        # print(self.query_tokens)
        # print("N:")
        # print(self.query_ngrams)
        # print("dependencies:")
        # print(self.dependencies)


        # DETECT EXPLICIT AND IMPLICIT ATTRIBUTES
        self.extracted_attributes = self.attribute_genie_instance.extract_attributes(self.query_ngrams)



        # DETECT IMPLICIT AND EXPLICIT TASKS
        task_map = self.task_genie_instance.extract_explicit_tasks_from_dependencies(self.dependencies)
        # print(task_map)

        # Filters from Domain Values
        task_map = self.task_genie_instance.extract_explicit_tasks_from_domain_value(task_map)
        # print(task_map)
        # At this stage, which attributes are encodeable?
        encodeable_attributes = self.attribute_genie_instance.get_encodeable_attributes()
        # INFER tasks based on (encodeable) attribute Datatypes
        task_map = self.task_genie_instance.extract_implicit_tasks_from_attributes(task_map, encodeable_attributes)
        # From the generated TaskMap, ensure that the task "keys" are NOT EMPTY LISTS
        # print(task_map)
        self.extracted_tasks = self.task_genie_instance.filter_empty_tasks(task_map)


        # RECOMMEND VISUALIZATIONS FROM ATTRIBUTES, TASKS, and VISUALIZATIONS

        # Final list of encodeable attributes in the VIS
        final_encodeable_attributes = self.attribute_genie_instance.update_encodeable_attributes_based_on_tasks()


        # Prepare output
        output = {
            'query_raw': self.query_raw,
            'query': self.query_processed,
            'dataset': self.data_url,
            'attributeMap': self.extracted_attributes,
            'taskMap': self.extracted_tasks,
        }

        return output if debug else helpers.delete_keys_from_dict(output, keys=constants.keys_to_delete_in_output)

    # Update the attribute datatypes that were not correctly detected by NL4DV
    def set_attribute_datatype(self, attr_type_obj):
        return self.data_genie_instance.set_attribute_datatype(attr_type_obj=attr_type_obj)

    # Set Label attribute for the dataset, i.e. one that defines what the dataset is about.
    # e.g. "Correlate horsepower and MPG for sports car models" should NOT apply an explicit attribute for models since there are two explicit attributes already present.
    def set_label_attribute(self, label_attribute):
        return self.data_genie_instance.set_label_attribute(label_attribute=label_attribute)

    # WORDS that should be IGNORED in the query, i.e. NOT lead to the detection of attributes and tasks
    # `Movie` in movies dataset
    # `Car` in cars dataset
    def set_ignore_words(self, ignore_words):
        return self.data_genie_instance.set_ignore_words(ignore_words=ignore_words)

    # Custom STOPWORDS that should NOT removed from the query, as they might be present in the domain.
    # e.g. `A` in grades dataset
    def set_reserve_words(self, reserve_words):
        return self.data_genie_instance.set_reserve_words(reserve_words=reserve_words)

    # Sets the AliasMap
    def set_alias_map(self, alias_map=None, alias_url=None):
        return self.data_genie_instance.set_alias_map(alias_map=alias_map, alias_url=alias_url)

    # Sets the Dataset
    def set_data(self, data_url=None):
        return self.data_genie_instance.set_data(data_url=data_url)

    # Sets the String Matching, Domain Word Limit, ... Thresholds
    def set_thresholds(self, thresholds):
        for t in thresholds:
            if t in self.match_thresholds and (isinstance(thresholds[t], float) or isinstance(thresholds[t], int)):
                self.match_thresholds[t] = thresholds[t]
        return True

    # Sets the Scoring Weights for the way attributes / tasks and visualizations are detected.
    def set_importance_scores(self, scores):
        for s in scores.keys():
            if s in self.match_scores and isinstance(scores[s], float):
                self.match_scores[s] = scores[s]

        return True

    # Get the dataset metadata
    def get_metadata(self):
        return self.data_genie_instance.data_attribute_map

    # Create a dependency parser instance
    def set_dependency_parser(self, config):
        if isinstance(config, dict):
            helpers.cond_print("Dependency Parser: " + config["name"], self.verbose)
            self.dependency_parser = config["name"]
            if config["name"] == "spacy":
                """
                    Sets the model and returns the Spacy NLP instance. Example ways from the Spacy docs:
                    spacy.load("en") # shortcut link
                    spacy.load("en_core_web_sm") # package
                    spacy.load("/path/to/en") # unicode path
                    spacy.load(Path("/path/to/en")) # pathlib Path
                """
                self.dependency_parser_instance = spacy.load(config["model"])

            elif config["name"] == "corenlp":
                if 'CLASSPATH' not in os.environ:
                    os.environ['CLASSPATH'] = ""

                cpath = config["model"] + os.pathsep + config["parser"]
                if cpath not in os.environ['CLASSPATH']:
                    os.environ['CLASSPATH'] = cpath + os.pathsep + os.environ['CLASSPATH']

                # TODO:- DEPRECATED
                self.dependency_parser_instance = StanfordDependencyParser(path_to_models_jar=config["model"],
                                                                           encoding='utf8')
            elif config["name"] == "corenlp-server":
                # Requires the CoreNLPServer running in the background at the below URL (generally https://localhost:9000)
                # Start server by running the following command in the JARs directory.
                # `java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -annotators "tokenize,ssplit,pos,lemma,parse,sentiment" -port 9000 -timeout 30000`
                self.dependency_parser_instance = CoreNLPDependencyParser(url=config["url"])
