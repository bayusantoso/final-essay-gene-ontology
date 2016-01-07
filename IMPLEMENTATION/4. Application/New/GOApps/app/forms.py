from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, SelectField
from wtforms.validators import DataRequired

class SearchForm(Form):
  query = StringField('query')
  relationship = SelectField('relationship',choices=[('children','Children'),('parent','Parent'),('anchestor','Anchestor'),('offspring','Offspring')])
  ontology = SelectField('relationship',choices=[('BP','Biological Process'),('CC','Cellular Compontent'),('MF','Moleculare Function')])

class SimilarityForm(Form):
  first_go_id = StringField('first_go_id')
  second_go_id = StringField('second_go_id')
  similarity_function = SelectField('similarity_function',choices=[('cosine','Cosine Similarity'),('CC','Cellular Compontent'),('MF','Moleculare Function')])
