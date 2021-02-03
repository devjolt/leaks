from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django.forms.widgets import NumberInput
from .models import LeakevidenceModel

class GateKeeperForm(forms.Form):
    Check_Box1 = forms.BooleanField(label = 'Home was vacant or the premises was unattended when the failure occurred', required = False)
    Check_Box2 = forms.BooleanField(label = 'Leak occurred at an industrial, commercial or institutional property', required = False)    
    Check_Box3 = forms.BooleanField(label = 'Leak occurred at a multi-residential property (ie. duplex, triplex, etc.)', required = False)
    Check_Box4 = forms.BooleanField(label = '''Leak was caused by outdoor water usage such as, but not limited to, pools, hot
tubs, hoses, irrigation systems or neglect of private property (ie. failing to winterize
outdoor taps)''', required = False)    
    Check_Box5 = forms.BooleanField(label = '''Usage was unexplained, due to purposeful damage (ie. broken pipe from
construction) or neglect (ie. failing to keep temperature inside home at acceptable
level)''', required = False)
    Check_Box6 = forms.BooleanField(label = 'The water utility account has previously been approved for the Customer Program', required = False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            'Check_Box1',
            'Check_Box2',
            'Check_Box3',
            'Check_Box4',
            'Check_Box5',
            'Check_Box6',
            Submit('submit', 'Submit', css_class = 'btn-success')
        )

class GateKeeperTwoForm(forms.Form):
    Check_Box7 = forms.BooleanField(label = 'Did the leak occur at a single family home?', required = False)
    Check_Box8 = forms.BooleanField(label = '''Was the monthly water usage during the leak at least three times your average
monthly consumption?''', required = False)    
    Check_Box9 = forms.BooleanField(label = 'Was the leak repaired in the last 2 months?', required = False)
    Check_Box10 = forms.BooleanField(label = '''Was a decrease in your monthly water usage observed AFTER the leak was
repaired?''', required = False)    
    Check_Box11 = forms.BooleanField(label = '''Is the plumbing in compliance with government regulations?''', required = False)
    Check_Box12 = forms.BooleanField(label = 'Is this your first time applying for the one-time customer assistance program?', required = False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            'Check_Box7',
            'Check_Box8',
            'Check_Box9',
            'Check_Box10',
            'Check_Box11',
            'Check_Box12',
            Submit('submit', 'Submit', css_class = 'btn-success')
        )

class LeakFormOne(forms.Form):
    BillingNum = forms.IntegerField(label = '''Billing number found
on London Hydro bill''') #max_length = 10, min_length = 5)
    Type_of_Name = forms.ChoiceField(widget=forms.RadioSelect, choices=[
        ('mr', 'Mr'),
        ('mrs', 'Mrs'),
        ('ms', 'Ms'),
        ], 
        label = 'Title')
    AcctHolder = forms.CharField(label = 'Account holder name')
    PhoneNum = forms.IntegerField(label = 'Numbers only')#forms.RegexField()
    Extension = forms.IntegerField()#forms.RegexField()
    Email = forms.EmailField(label='Email')

class LeakFormTwo(forms.Form):
    UnitNum = forms.IntegerField(label = 'Unit no.')
    StreetNum = forms.IntegerField(label = 'Street number')
    StreetName = forms.IntegerField(label = 'Street name including suffix')
    Drection = forms.CharField(label = 'Drection')
    City = forms.CharField(label = 'City')
    PostalCode = forms.CharField(label = 'Postal Code')# regex = "G.*s")

class LeakFormThree(forms.Form):
    DescribeRepair = forms.CharField(widget=forms.Textarea)
    RepairDate = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    MeterNum = forms.DecimalField()
    MeterReading =forms.DecimalField()
    PipeLeak = forms.BooleanField(required = False)
    ValveLeak = forms.BooleanField(required = False)
    FittingLeak = forms.BooleanField(required = False)
    ToiletLeak = forms.BooleanField(required = False)
    OtherLeak = forms.BooleanField(required = False)
    ddlTypeOfPipe = forms.ChoiceField(choices=[
        ('lead', 'Lead'), 
        ('copper', 'Copper'), 
        ('plastic', 'Plastic'), 
        ('other', 'Other')])
    Explain = forms.CharField(widget=forms.Textarea)

class LeakFormFour(forms.Form):
    HWReceipts = forms.BooleanField(required = False)
    PlumbersInvoices = forms.BooleanField(required = False)
    Photos = forms.BooleanField(required = False)

#this is the skizzle

from .models import LeakevidenceModel

class MeternoForm(forms.Form):
    meterno = forms.CharField(max_length = 5)

class LeakevidenceForm(forms.ModelForm):
    class Meta:
        model = LeakevidenceModel
        fields = ('files',)


'''
            'UnitNum',
            'Drection',
            'City',
            'PostalCode',
            'Type of Name',
            'Extension',
            'PipeLeak',
            'ValveLeak',
            'FittingLeak',
            'ToiletLeak',
            'OtherLeak',
            'Explain',
            'StreetNum',
            'StreetName',
            'BillingNum',
            'MeterNum',
            'AcctHolder',
            'PhoneNum',
            'Email',
            'DescribeRepair',
            'RepairDate',
            'MeterReading',
            'Repairs',
            'ddlTypeOfPipe',
            'HWReceipts',
            'PlumbersInvoices',
            'Photos',


BillingNum = forms.CharField()
    UnitNum = forms.DecimalField()
    StreetName = forms.CharField()
    StreetNum = forms.CharField()#forms.RegexField()
    Drection = forms.CharField()
    City = forms.CharField()
    PostalCode = forms.CharField()#forms.RegexField()
    Type_of_Name = forms.ChoiceField(widget=forms.RadioSelect, choices=[
        ('mr', 'Mr'),
        ('mrs', 'Mrs'),
        ('ms', 'Ms'),])
    #Type of Name other = forms.CharField()
    PhoneNum = forms.CharField()#forms.RegexField()
    Extension = forms.CharField()#forms.RegexField()
    Email = forms.EmailField(label='Email')
    DescribeRepair = forms.CharField(widget=forms.Textarea)
    RepairDate = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    MeterNum = forms.DecimalField()
    MeterReading =forms.DecimalField()
    PipeLeak = forms.BooleanField(required = False)
    ValveLeak = forms.BooleanField(required = False)
    FittingLeak = forms.BooleanField(required = False)
    ToiletLeak = forms.BooleanField(required = False)
    OtherLeak = forms.BooleanField(required = False)
    Explain = forms.CharField(widget=forms.Textarea)
    ddlTypeOfPipe = forms.ChoiceField(choices=[
        ('lead', 'Lead'), 
        ('copper', 'Copper'), 
        ('plastic', 'Plastic'), 
        ('other', 'Other')])
    HWReceipts = forms.CharField(widget=forms.Textarea)
    PlumbersInvoices = forms.BooleanField()
    Photos = forms.BooleanField(required = False)
    FittingLeak = forms.BooleanField(required = False)
    ToiletLeak = forms.BooleanField(required = False)
'''