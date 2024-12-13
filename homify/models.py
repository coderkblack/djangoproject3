from django.db import models

# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.email}"

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        db_table = 'clients'

class Houses(models.Model):
    name = models.CharField(max_length=100)
    developer = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.address} - {self.city}"

    class Meta:
        verbose_name = 'House'
        verbose_name_plural = 'Houses'
        ordering = ['address', 'city', 'state', 'country']
        db_table = 'houses'

class Onsale(models.Model):
    house = models.ForeignKey(Houses, on_delete=models.CASCADE)
    customer = models.ForeignKey(Client, on_delete=models.CASCADE)
    status = models.CharField(max_length=100) #Fully paid, Partially paid
    deadline_of_payment = models.DateField()
    completed_payment = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.house} - {self.customer}"

    @property
    def total_fine(self):
        if self.completed_payment and self.deadline_of_payment and self.completed_payment > self.deadline_of_payment:
            amount = (self.completed_payment - self.deadline_of_payment).days * 1000
            return amount
        return 0

    @property
    def overdue_days(self):
        if self.completed_payment and self.deadline_of_payment and self.completed_payment > self.deadline_of_payment:
            days = (self.completed_payment - self.deadline_of_payment).days
            return days
        return 0

    class Meta:
        verbose_name = 'Onsale'
        verbose_name_plural = 'Onsales'
        ordering= ['-created_at']
        db_table = 'onsale'

class Payment(models.Model):
    onsale = models.ForeignKey(Onsale, on_delete=models.CASCADE)
    merchant_request_id = models.CharField(max_length=100)
    checkout_request_id = models.CharField(max_length=100)
    code = models.CharField(max_length=30, null=True)
    amount = models.IntegerField(max_length=20)
    status = models.CharField(max_length=20, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-created_at']
        db_table = 'payments'
        def __str__(self):
            return f"{self.merchant_request_id} - {self.code}"