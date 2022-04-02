from basic import models
from django.db.models import (
    Case, When, Value, Q, F, ExpressionWrapper, FloatField, DurationField, DateField, IntegerField, Func, DateTimeField,
    CharField, Sum
)
from django.db.models.functions import Now, Cast, ExtractDay, ExtractYear, Extract, LPad, Upper, Lower


def utilizando_case():
    return models.Employee.objects.annotate(
        gender_description=Case(
            When(gender=models.ModelBase.Gender.MALE, then=Value('Masculino')),
            default=Value('Feminino')
        )
    )


def exercicio1():
    return models.Employee.objects.annotate(
        status=Case(
            When(salary__lte=2000, then=Value('Vendedor Jr')),
            When(Q(salary__gt=2000) & Q(salary__lte=5000), then=Value('Vendedor Pleno')),
            default=Value('Vendedor Sênior')
        )
    )


def exercicio2():
    return models.Employee.objects.annotate(
        bairro=F('district__name'),
        cidade=F('district__city__name'),
        estado=F('district__city__state__name')
    ).values('name', 'bairro', 'cidade', 'estado')


def exercicio3():
    return models.Employee.objects.values(
        'name',
        'district__name',
        'district__city__name',
        'district__city__state__name'
    )


def exercicio4(quantity):
    return models.Product.objects.annotate(
        subtotal=ExpressionWrapper(F('sale_price') * quantity, output_field=FloatField()),
        commission=ExpressionWrapper(
            F('subtotal') * F('product_group__commission_percentage') / 100, output_field=FloatField()
        )
    ).values('name', 'sale_price', 'subtotal', 'product_group__commission_percentage', 'commission')


def exercicio5():
    # return models.Employee.objects.filter(
    #     Q(marital_status__name__icontains='casado') |
    #     Q(marital_status__name__icontains='solteiro')
    # )
    return models.Employee.objects.filter(
        marital_status__name__in=['Solteiro', 'Casado']
    )


def exercicio6():
    # return models.Employee.objects.filter(salary__range=(1000, 5000))
    return models.Employee.objects.filter(salary__gte=1000, salary__lte=5000)


def exercicio7():
    return models.Product.objects.annotate(
        diff=ExpressionWrapper(F('sale_price') - F('cost_price'), output_field=FloatField())
    ).values('name', 'sale_price', 'cost_price', 'diff')


def execicio8():
    return models.Employee.objects.exclude(salary__range=(4000, 8000))


def exercicio9():
    return models.Sale.objects.filter(date__year__range=(2010, 2021))


def exercicio10():
    # return models.Employee.objects.annotate(
    #     diff=ExpressionWrapper(Cast(Now(), output_field=DateField()) - F('birth_date'), output_field=DurationField()),
    #     age=ExpressionWrapper(ExtractDay(F('diff')) / 365, output_field=IntegerField()),
    #     status=Case(
    #         When(age__range=(18, 25), then=Value('Vendedor Jr.')),
    #         When(age__range=(26, 34), then=Value('Vendedor Pleno')),
    #         When(age__gte=35, then=Value('Vendedor Sênior')),
    #         default=Value('Não econtrado')
    #     )
    # ).values('name', 'age', 'status')

    return models.Employee.objects.annotate(
        age=ExtractYear(Func(F('birth_date'), function='age'))
    ).values('name', 'age')


def exercicio11():
    return models.Customer.objects.annotate(
        gender_description=Case(
            When(gender=models.ModelBase.Gender.MALE, then=Value('Masculino')),
            default=Value('Feminino')
        )
    )


def exercicio12():
    return models.Employee.objects.annotate(
        code=LPad(Cast(F('id'), output_field=CharField()), 5, Value('0'))
    ).values('code', 'id', 'name')


def exercicio13():
    return models.Employee.objects.annotate(
        _upper=Upper('name'),
        _lower=Lower('name')
    ).values('_upper', '_lower')


def exercicio14():
    return models.Employee.objects.select_related('department').values(
        'department__name', 'gender'
    ).annotate(
        sum=Sum('salary')
    ).values('department__name', 'gender', 'sum')


def exercicio15():
    # Fazer uma consulta para retornar o nome do funcionário e o bairro onde ele mora;
    return models.Employee.objects.values('name', 'district__name')


def exercicio16():
    # Fazer uma consulta para retornar o nome do cliente, cidade e zona que o mesmo mora;
    return models.Customer.objects.values(
        'name', 'district__name', 'district__zone__name', 'district__city__name'
    )


def exercicio17():
    # Fazer uma consulta para retornar os dados da filial, estado e cidade onde a mesma está localizada;
    return models.Branch.objects.values(
        'name', 'district__city__state__name', 'district__city__name'
    )


def exercicio18():
    # Fazer uma consulta par retornar os dados do funcionário, departamento onde ele trabalha e
    # qual seu estado civil atual
    return models.Employee.objects.values(
        'name', 'department__name', 'marital_status__name'
    )


def exercicio19():
    # Fazer uma consulta para retornar o nome do produto vendido, o preço unitário e o subtotal;
    return models.SaleItem.objects.annotate(
        subtotal=ExpressionWrapper(F('quantity') * F('product__sale_price'), FloatField()),
    ).values('product__name', 'product__sale_price', 'subtotal')
    # return models.SaleItem.objects.annotate(
    #     subtotal=ExpressionWrapper(F('quantity') * F('product__sale_price'), FloatField())
    # ).values('product__name').annotate(
    #     total=Sum('subtotal')
    # ).values('product__name', 'total')


def exercicio20(commission=True):
    field = 'product__product_group__commission_percentage'
    if not commission:
        field = 'product__product_group__gain_percentage'
    # Fazer uma consulta para retornar o nome do produto, subtotal e quanto deve ser pago de comissão por cada item;
    return models.SaleItem.objects.select_related('product__product_group').annotate(
        subtotal=ExpressionWrapper(F('quantity') * F('product__sale_price'), output_field=FloatField()),
        commission_or_gain=ExpressionWrapper(
            F('subtotal') * (F(field) / 100),
            output_field=FloatField()
        )
    ).values(
        'product__name', 'product__sale_price', 'subtotal',
        'product__product_group__commission_percentage',
        'commission_or_gain'
    )


def exercicio21():
    # Ranking dos 10 funcionários mais bem pagos;
    return models.Employee.objects.order_by('-salary').values('name', 'salary')[:10]


def exercicio22():
    # Ranking dos 20 clientes que tem a menor renda mensal;
    return models.Customer.objects.order_by('income').values('name', 'income')[:20]


def exercicio23():
    # Trazer do décimo primeiro ao vigésimo funcionário mais bem pago;
    return models.Employee.objects.order_by('-salary')[10:20]


#
# def exercicio21():
#     # Fazer uma consulta para retornar o nome do produto, subtotal e quanto deve ser pago de comissão por cada item;
#     return models.SaleItem.objects.select_related('product__product_group').annotate(
#         subtotal=ExpressionWrapper(F('quantity') * F('product__sale_price'), output_field=FloatField()),
#         gain=ExpressionWrapper(
#             F('subtotal') * (F('product__product_group__gain_percentage') / 100),
#             output_field=FloatField()
#         )
#     ).values(
#         'product__name', 'product__sale_price', 'subtotal',
#         'product__product_group__commission_percentage',
#         'commission'
#     )


"""
[ok] - Fazer uma consulta para retornar todos os funcionários casados ou solteiros;
[ok] - Fazer uma consulta para retornar todos os funcionários que ganham entre R$ 1.000,00 e R$ 5.000,00;
[ok] - Fazer uma consulta que retorne a diferença do preço de custo e preço de venda dos produtos;
[ok] - Fazer uma consulta para retornar todos os funcionários que não tenham salário entre R$ 4.000,00 e R$ 8.000,00;
[ok] - Fazer uma consulta para retornar todas as vendas entre 2010 e 2021;
[ok] - Fazer uma consulta que retorne o tipo de funcionário de acordo com a sua idade.
    18 - 25 - Jr.
    26 - 34 - Pl.
    35 ou mais - Sr.   
Fazer uma consulta para retornar um status para o funcionário de acordo com o tempo de casa.
    Até 2 anos - Novato
    Acima 2 anos e menor ou igual a 5 anos - Intermediário 
    Acima de 5 anos - Veterano

[ok] - Fazer uma consulta para retornar o nome do funcionário e o bairro onde ele mora;
[ok] - Fazer uma consulta para retornar o nome do cliente, cidade e zona que o mesmo mora;
[ok] - Fazer uma consulta para retornar os dados da filial, estado e cidade onde a mesma está localizada;
[ok] - Fazer uma consulta par retornar os dados do funcionário, departamento onde ele trabalha e qual seu estado civil atual;
[ok] - Fazer uma consulta para retornar o nome do produto vendido, o preço unitário e o subtotal;
[ok] - Fazer uma consulta para retornar o nome do produto, subtotal e quanto deve ser pago de comissão por cada item;
[ok] - Fazer uma consulta para retornar o nome do produto, subtotal e quanto foi obtido de lucro por item;
[ok] - Ranking dos 10 funcionários mais bem pagos;
[ok] - Ranking dos 20 clientes que tem a menor renda mensal;
[ok] - Trazer do décimo primeiro ao vigésimo funcionário mais bem pago;
Ranking dos produtos mais caros vendidos no ano de 2021;
Criar uma consulta para trazer o primeiro nome dos funcionários.
    Sr. Sra. Dr. Dra. remover se tiver.
Criar uma consulta para trazer o último nome dos clientes.
Criar uma consulta para rocar quem tenha silva no nome para Oliveira.
Criar uma consulta para trazer o total de funcionários por estado civil;
Criar uma consulta para trazer o total vendido em valor R$ por filial;
Criar uma consulta para trazer o total vendido em valor R$ por zona;
Criar uma consulta para trazer o total vendido em valor R$ por estado;
Criar uma consulta para trazer o total vendido em quantidade por cidade, trazer apenas as cidades que tiveram vendas acima de quantidade 100;
Trazer a media de salários por sexo, o sexo deve está de forma descritiva;
Fazer uma consulta que retorne os 5 grupos de produtos mais lucrativos em termos de valor, os grupos só entram na lista com lucros acima de R$ 200,00;
Uma consulta para trazer a média de salários por departamento;
Uma consulta para trazer o total vendido em valor por ano;
Uma consulta para trazer o total vendido em valor por idade de funcionário;

"""
