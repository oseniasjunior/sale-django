from basic import models


class EmployeeActions:
    @staticmethod
    def adjustment_salary(percentage, employee):
        pass


class SaleActions:
    @staticmethod
    def sale_by_year():
        results = models.Sale.objects.by_year()
        results = map(lambda item: f"{item['year']}, {item['month']}, {item['total']}\n", results)
        with open('sale_by_year.txt', 'a') as file:
            file.writelines(results)
