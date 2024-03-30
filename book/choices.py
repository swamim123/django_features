from djchoices import DjangoChoices, ChoiceItem


class OrgnizationTypeChoices(DjangoChoices):
    ENERGY = ChoiceItem("ENE")
    IOT = ChoiceItem("IOT")
    FINSERV = ChoiceItem("FIS")