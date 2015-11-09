from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, SelectField
from wtforms.validators import DataRequired

class SearchForm(Form):
  query = StringField('query')
  relationship = SelectField('relationship',choices=[('children','Children'),('parent','Parent'),('anchestor','Anchestor'),('offspring','Offspring')])
  ontology = SelectField('relationship',choices=[('BP','Biological Process'),('CC','Cellular Compontent'),('MF','Moleculare Function')])
