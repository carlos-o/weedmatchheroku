import serpy


class CreditCardSerializers(serpy.Serializer):
    """
        this class converts the data of the weedmatch user's credit card into json
    """
    id = serpy.Field()
    first_name = serpy.Field()
    last_name = serpy.Field()
    type_card = serpy.Field()
    number_card = serpy.MethodField()
    month = serpy.MethodField()
    year = serpy.MethodField()

    def get_number_card(self, obj):
        """
            this method obtain the last fourth digits of credit card number

            :param obj: credit card  object
            :type obj: Model CreditCard
            :return: The last fourth digits of credit card number
        """
        if not obj.number_card:
            return ""
        return obj.number_card[-4:]

    def get_month(self, obj):
        """
            This method obtain the month of expiration credit card

            :param obj: credit card  object.
            :type obj: Model CreditCard.
            :return: The month of expiration date
        """
        if not obj.date_expiration:
            return ""
        month = str(obj.date_expiration)
        return month[5:7]

    def get_year(self, obj):
        """
            This method obtain the year of expiration credit card

           :param obj: credit card  object.
           :type obj: Model CreditCard.
           :return: The year of expiration date
        """
        if not obj.date_expiration:
            return ""
        month = str(obj.date_expiration)
        return month[2:4]
