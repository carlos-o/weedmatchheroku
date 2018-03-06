import serpy


class CreditCardSerializers(serpy.Serializer):
    id = serpy.Field()
    first_name = serpy.Field()
    last_name = serpy.Field()
    type_card = serpy.Field()
    number_card = serpy.MethodField()
    month = serpy.MethodField()
    year = serpy.MethodField()

    def get_number_card(self, obj):
        return obj.number_card[-4:]

    def get_month(self, obj):
        month = str(obj.date_expiration)
        return month[5:7]

    def get_year(self, obj):
        month = str(obj.date_expiration)
        return month[2:4]
