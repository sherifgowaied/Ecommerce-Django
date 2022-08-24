#from django_countries.fields import CountryField
from email.policy import default
from attr import attr
from django import forms
# django_countries.fields import CountryField
from django import forms

PAYMENT_CHOICES =(
    ("P","Paypal"),
    ("S","Stripe")
)
COUNTRIES = (
    ('', 'Select a Country'),
    ('AF', ('Afghanistan')),
    ('AX', ('Aland Islands')),
    ('AL', ('Albania')),
    ('DZ', ('Algeria')),
    ('AS', ('American Samoa')),
    ('AD', ('Andorra')),
    ('AO', ('Angola')),
    ('AI', ('Anguilla')),
    ('AQ', ('Antarctica')),
    ('AG', ('Antigua and Barbuda')),
    ('AR', ('Argentina')),
    ('AM', ('Armenia')),
    ('AW', ('Aruba')),
    ('AU', ('Australia')),
    ('AT', ('Austria')),
    ('AZ', ('Azerbaijan')),
    ('BS', ('Bahamas')),
    ('BH', ('Bahrain')),
    ('BD', ('Bangladesh')),
    ('BB', ('Barbados')),
    ('BY', ('Belarus')),
    ('BE', ('Belgium')),
    ('BZ', ('Belize')),
    ('BJ', ('Benin')),
    ('BM', ('Bermuda')),
    ('BT', ('Bhutan')),
    ('BO', ('Bolivia')),
    ('BA', ('Bosnia and Herzegovina')),
    ('BW', ('Botswana')),
    ('BV', ('Bouvet Island')),
    ('BR', ('Brazil')),
    ('IO', ('British Indian Ocean Territory')),
    ('BN', ('Brunei Darussalam')),
    ('BG', ('Bulgaria')),
    ('BF', ('Burkina Faso')),
    ('BI', ('Burundi')),
    ('KH', ('Cambodia')),
    ('CM', ('Cameroon')),
    ('CA', ('Canada')),
    ('CV', ('Cape Verde')),
    ('KY', ('Cayman Islands')),
    ('CF', ('Central African Republic')),
    ('TD', ('Chad')),
    ('CL', ('Chile')),
    ('CN', ('China')),
    ('CX', ('Christmas Island')),
    ('CC', ('Cocos (Keeling) Islands')),
    ('CO', ('Colombia')),
    ('KM', ('Comoros')),
    ('CG', ('Congo')),
    ('CD', ('Congo, The Democratic Republic of the')),
    ('CK', ('Cook Islands')),
    ('CR', ('Costa Rica')),
    ('CI', ('Cote d\'Ivoire')),
    ('HR', ('Croatia')),
    ('CU', ('Cuba')),
    ('CY', ('Cyprus')),
    ('CZ', ('Czech Republic')),
    ('DK', ('Denmark')),
    ('DJ', ('Djibouti')),
    ('DM', ('Dominica')),
    ('DO', ('Dominican Republic')),
    ('EC', ('Ecuador')),
    ('EG', ('Egypt')),
    ('SV', ('El Salvador')),
    ('GQ', ('Equatorial Guinea')),
    ('ER', ('Eritrea')),
    ('EE', ('Estonia')),
    ('ET', ('Ethiopia')),
    ('FK', ('Falkland Islands (Malvinas)')),
    ('FO', ('Faroe Islands')),
    ('FJ', ('Fiji')),
    ('FI', ('Finland')),
    ('FR', ('France')),
    ('GF', ('French Guiana')),
    ('PF', ('French Polynesia')),
    ('TF', ('French Southern Territories')),
    ('GA', ('Gabon')),
    ('GM', ('Gambia')),
    ('GE', ('Georgia')),
    ('DE', ('Germany')),
    ('GH', ('Ghana')),
    ('GI', ('Gibraltar')),
    ('GR', ('Greece')),
    ('GL', ('Greenland')),
    ('GD', ('Grenada')),
    ('GP', ('Guadeloupe')),
    ('GU', ('Guam')),
    ('GT', ('Guatemala')),
    ('GG', ('Guernsey')),
    ('GN', ('Guinea')),
    ('GW', ('Guinea-Bissau')),
    ('GY', ('Guyana')),
    ('HT', ('Haiti')),
    ('HM', ('Heard Island and McDonald Islands')),
    ('VA', ('Holy See (Vatican City State)')),
    ('HN', ('Honduras')),
    ('HK', ('Hong Kong')),
    ('HU', ('Hungary')),
    ('IS', ('Iceland')),
    ('IN', ('India')),
    ('ID', ('Indonesia')),
    ('IR', ('Iran, Islamic Republic of')),
    ('IQ', ('Iraq')),
    ('IE', ('Ireland')),
    ('IM', ('Isle of Man')),
    ('IL', ('Israel')),
    ('IT', ('Italy')),
    ('JM', ('Jamaica')),
    ('JP', ('Japan')),
    ('JE', ('Jersey')),
    ('JO', ('Jordan')),
    ('KZ', ('Kazakhstan')),
    ('KE', ('Kenya')),
    ('KI', ('Kiribati')),
    ('KP', ('Korea, Democratic People\'s Republic of')),
    ('KR', ('Korea, Republic of')),
    ('KW', ('Kuwait')),
    ('KG', ('Kyrgyzstan')),
    ('LA', ('Lao People\'s Democratic Republic')),
    ('LV', ('Latvia')),
    ('LB', ('Lebanon')),
    ('LS', ('Lesotho')),
    ('LR', ('Liberia')),
    ('LY', ('Libyan Arab Jamahiriya')),
    ('LI', ('Liechtenstein')),
    ('LT', ('Lithuania')),
    ('LU', ('Luxembourg')),
    ('MO', ('Macao')),
    ('MK', ('Macedonia, The Former Yugoslav Republic of')),
    ('MG', ('Madagascar')),
    ('MW', ('Malawi')),
    ('MY', ('Malaysia')),
    ('MV', ('Maldives')),
    ('ML', ('Mali')),
    ('MT', ('Malta')),
    ('MH', ('Marshall Islands')),
    ('MQ', ('Martinique')),
    ('MR', ('Mauritania')),
    ('MU', ('Mauritius')),
    ('YT', ('Mayotte')),
    ('MX', ('Mexico')),
    ('FM', ('Micronesia, Federated States of')),
    ('MD', ('Moldova')),
    ('MC', ('Monaco')),
    ('MN', ('Mongolia')),
    ('ME', ('Montenegro')),
    ('MS', ('Montserrat')),
    ('MA', ('Morocco')),
    ('MZ', ('Mozambique')),
    ('MM', ('Myanmar')),
    ('NA', ('Namibia')),
    ('NR', ('Nauru')),
    ('NP', ('Nepal')),
    ('NL', ('Netherlands')),
    ('AN', ('Netherlands Antilles')),
    ('NC', ('New Caledonia')),
    ('NZ', ('New Zealand')),
    ('NI', ('Nicaragua')),
    ('NE', ('Niger')),
    ('NG', ('Nigeria')),
    ('NU', ('Niue')),
    ('NF', ('Norfolk Island')),
    ('MP', ('Northern Mariana Islands')),
    ('NO', ('Norway')),
    ('OM', ('Oman')),
    ('PK', ('Pakistan')),
    ('PW', ('Palau')),
    ('PS', ('Palestinian Territory, Occupied')),
    ('PA', ('Panama')),
    ('PG', ('Papua New Guinea')),
    ('PY', ('Paraguay')),
    ('PE', ('Peru')),
    ('PH', ('Philippines')),
    ('PN', ('Pitcairn')),
    ('PL', ('Poland')),
    ('PT', ('Portugal')),
    ('PR', ('Puerto Rico')),
    ('QA', ('Qatar')),
    ('RE', ('Reunion')),
    ('RO', ('Romania')),
    ('RU', ('Russian Federation')),
    ('RW', ('Rwanda')),
    ('BL', ('Saint Barthelemy')),
    ('SH', ('Saint Helena')),
    ('KN', ('Saint Kitts and Nevis')),
    ('LC', ('Saint Lucia')),
    ('MF', ('Saint Martin')),
    ('PM', ('Saint Pierre and Miquelon')),
    ('VC', ('Saint Vincent and the Grenadines')),
    ('WS', ('Samoa')),
    ('SM', ('San Marino')),
    ('ST', ('Sao Tome and Principe')),
    ('SA', ('Saudi Arabia')),
    ('SN', ('Senegal')),
    ('RS', ('Serbia')),
    ('SC', ('Seychelles')),
    ('SL', ('Sierra Leone')),
    ('SG', ('Singapore')),
    ('SK', ('Slovakia')),
    ('SI', ('Slovenia')),
    ('SB', ('Solomon Islands')),
    ('SO', ('Somalia')),
    ('ZA', ('South Africa')),
    ('GS', ('South Georgia and the South Sandwich Islands')),
    ('ES', ('Spain')),
    ('LK', ('Sri Lanka')),
    ('SD', ('Sudan')),
    ('SR', ('Suriname')),
    ('SJ', ('Svalbard and Jan Mayen')),
    ('SZ', ('Swaziland')),
    ('SE', ('Sweden')),
    ('CH', ('Switzerland')),
    ('SY', ('Syrian Arab Republic')),
    ('TW', ('Taiwan, Province of China')),
    ('TJ', ('Tajikistan')),
    ('TZ', ('Tanzania, United Republic of')),
    ('TH', ('Thailand')),
    ('TL', ('Timor-Leste')),
    ('TG', ('Togo')),
    ('TK', ('Tokelau')),
    ('TO', ('Tonga')),
    ('TT', ('Trinidad and Tobago')),
    ('TN', ('Tunisia')),
    ('TR', ('Turkey')),
    ('TM', ('Turkmenistan')),
    ('TC', ('Turks and Caicos Islands')),
    ('TV', ('Tuvalu')),
    ('UG', ('Uganda')),
    ('UA', ('Ukraine')),
    ('AE', ('United Arab Emirates')),
    ('GB', ('United Kingdom')),
    ('US', ('United States')),
    ('UM', ('United States Minor Outlying Islands')),
    ('UY', ('Uruguay')),
    ('UZ', ('Uzbekistan')),
    ('VU', ('Vanuatu')),
    ('VE', ('Venezuela')),
    ('VN', ('Viet Nam')),
    ('VG', ('Virgin Islands, British')),
    ('VI', ('Virgin Islands, U.S.')),
    ('WF', ('Wallis and Futuna')),
    ('EH', ('Western Sahara')),
    ('YE', ('Yemen')),
    ('ZM', ('Zambia')),
    ('ZW', ('Zimbabwe')),
)

# class CountryField(forms.ChoiceField):
#     def __init__(self, *args, **kwargs):
#         kwargs.setdefault('choices', COUNTRIES)

#         super(CountryField, self).__init__(*args, **kwargs)

class ChekoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_country =forms.ChoiceField(choices=COUNTRIES , required=False ,widget=forms.Select(attrs={
       "class":"custom-select d-block w-100",
        "id":"country",
        "placeholder":"Select a country",
    }))
    shipping_zip = forms.CharField(required=False)

    billing_address = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_country =forms.ChoiceField(choices=COUNTRIES , required=False ,widget=forms.Select(attrs={
       "class":"custom-select d-block w-100",
        "id":"country",
        "placeholder":"Select a country",
    }))
    billing_zip = forms.CharField(required=False)

    same_billing_address = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False) 
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False) 
    
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(),choices=PAYMENT_CHOICES)


class CouponForm(forms.Form):
    code =forms.CharField(widget=forms.TextInput(attrs={
        "class":'form-control',
        "placeholder":'Promo code',
        "aria-label" :"Recipient\ 's username",
        "aria-describedby" :"basic-addon2"
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField(widget=forms.TextInput(attrs={
        "class":"form-control" ,
        "id":"exampleInputPassword1"
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        "class":"form-control" ,
        "id":"exampleInputPassword1",
        "rows":4
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class":"form-control",
         "id":"exampleInputEmail1" ,
        "aria-describedby":"emailHelp"
    }))