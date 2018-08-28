from mongoengine import StringField, IntField, Document, EmbeddedDocument,ListField, EmbeddedDocumentField

class Offense(EmbeddedDocument):
    id = IntField(required=True, primary_key=True)
    offence_group = StringField(max_length=500)
    offence_type = StringField(max_length=500)
    incidents_2012 = StringField(required=True, max_length=500)
    rate_2012 = StringField(required=True, max_length=500)
    incidents_2013 = StringField(required=True, max_length=500)
    rate_2013 = StringField(required=True, max_length=500)
    incidents_2014 = StringField(required=True, max_length=500)
    rate_2014 = StringField(required=True, max_length=500)
    incidents_2015 = StringField(required=True, max_length=500)
    rate_2015 = StringField(required=True, max_length=500)
    incidents_2016 = StringField(required=True, max_length=500)
    rate_2016 = StringField(required=True, max_length=500)
    trend_24m = StringField(required=True, max_length=500)
    trend_60m = StringField(required=True, max_length=500)
    lga_rank = StringField(max_length=500)

    def __init__(self, id, offence_group, offence_type, incidents_2012, rate_2012, incidents_2013, rate_2013, \
                 incidents_2014, rate_2014, incidents_2015, rate_2015, incidents_2016, \
                 rate_2016, trend_24m, trend_60m, lga_rank, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = id
        self.offence_group = offence_group
        self.offence_type = offence_type
        self.incidents_2012 = incidents_2012
        self.rate_2012 = rate_2012
        self.incidents_2013 = incidents_2013
        self.rate_2013 = rate_2013
        self.incidents_2014 = incidents_2014
        self.rate_2014 = rate_2014
        self.incidents_2015 = incidents_2015
        self.rate_2015 = rate_2015
        self.incidents_2016 = incidents_2016
        self.rate_2016 = rate_2016
        self.trend_24m = trend_24m
        self.trend_60m = trend_60m
        self.lga_rank = lga_rank

class Area(Document):
    name = StringField(required=True)
    offenses = ListField(EmbeddedDocumentField(Offense))

    def __init__(self, name, offenses=[], *args, **values):
        super().__init__(*args, **values)
        self.name = name
        self.offenses = offenses
