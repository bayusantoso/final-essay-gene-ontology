class TermModel:
    go_id = ""
    term = ""
    ontology = ""
    definition = ""
    synonym = []
    secondary = []
    classes = []

    def set_go_id(self, value):
        self.go_id = value

    def get_go_id(self):
        return self.go_id

    def set_term(self, value):
        self.term = value

    def get_term(self):
        return self.term

    def set_ontology(self, value):
        self.ontology = value

    def get_ontology(self):
        return self.ontology

    def set_definition(self, value):
        self.definition = value

    def get_definition(self):
        return self.definition

    def set_synonym(self, value):
        self.synonym.append(value)

    def get_synonym(self):
        return self.synonym

    def set_secondary(self, value):
        self.secondary.append(value)

    def get_secondary(self):
        return self.secondary

    def set_classes(self, value):
        self.classes.append(value)

    def get_classes(self):
        return self.classes
