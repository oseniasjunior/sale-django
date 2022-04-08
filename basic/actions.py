from time import sleep

from basic import models, helpers


class EmployeeActions:
    @staticmethod
    def adjustment_salary(percentage, employee):
        pass


class SaleActions:
    @staticmethod
    def sale_by_year():
        results = models.Sale.objects.by_year()
        counter = results.count()
        results = map(lambda item: f"{item['year']}, {item['month']}, {item['total']}\n", results)
        with open('sale_by_year.txt', 'a') as file:
            for index, row in enumerate(results):
                file.write(row)
                percentage = (index / counter) * 100
                helpers.send_channel_message('chat', {'message': percentage})
                sleep(0.2)
