import dash
import pandas as pd
import os
import base64
import time

start_time = time.time()
external_stylesheets = ["https://fonts.googleapis.com/css?family=Raleway:300,400,600&display=swap",
    "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
    "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css", 
    'https://codepen.io/chriddyp/pen/bWLwgP.css']


# Configure app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
application = app.server
app.config.suppress_callback_exceptions = True
app.title = 'DA2i Dashboard'
# Import data
path = os.path.dirname(os.path.realpath('__file__')) + '/'

# df = pd.read_csv(path + 'DA2i_Database/DA2I_Indicator_Database.csv')
db_info = pd.read_csv(path + 'DA2i_Database/db_metadata_2020.csv')
country_info = pd.read_csv(path + 'DA2i_Database/country_info.csv')

indicator_info = pd.read_csv(path + 'DA2i_Database/db_indicator_info.csv')


# df = pd.read_csv(path + 'DA2i_Database/DA2I_Indicator_Database_Public.csv')
try:
  
    df = pd.read_csv(path + 'DA2i_Database/DA2I_Indicator_Database_Private.csv')

except:
    print("ERROR: error reading private database, will read public")
    df = pd.read_csv(path + 'DA2i_Database/DA2I_Indicator_Database_Public.csv')



df = df.merge(country_info, left_on='ISO3', right_on='ISO3', how='left')
df = df.merge(indicator_info, left_on='Name', right_on='Name', how='left')
df = df.merge(db_info, left_on='Source', right_on='Source', how='left')
# Map = pd.read_csv(path + 'DA2i_Database/Country_Flags.csv')
Map = country_info
df.sort_values(['Country', 'Name', 'Year'], inplace=True)

## Extract data to populate country drop-down list
countries = df.loc[df['ISO3'].notnull(), 'Country'].unique()
countries = [x for x in countries if str(x) != 'nan']

### Open and encode local images
image_filename = './assets/Connectivity_gravel.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

image_filename3 = './assets/GenderEquality_Gravel.png'
encoded_image3 = base64.b64encode(open(image_filename3, 'rb').read())

image_filename4 = './assets/equality_icon_gravel.png'
encoded_image4 = base64.b64encode(open(image_filename4, 'rb').read())

image_filename5 = './assets/Spyglass_Icon.png'
encoded_image5 = base64.b64encode(open(image_filename5, 'rb').read())

image_filename6 = './assets/Info_Icon_Purple.png'
encoded_image6 = base64.b64encode(open(image_filename6, 'rb').read())

image_filename7 = './assets/DA2I-2019-logo.jpg'
encoded_image7 = base64.b64encode(open(image_filename7, 'rb').read())