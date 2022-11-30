class city:

    def __init__(self, city_id, city_name):
        self.city_id = city_id
        self.city_name = city_name

    def __str__(self):
        return f"{self.city_id}, {self.city_name}"