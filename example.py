import pandas as pd
import hud_geo as czg

# Read in apikey
with open('config/hudkey','r') as o:
    hudkey = o.read()

# Lay out some examples
examplezip = '75035'
exampletract = '48113010801'

# Call classes against the different examples
h = czg.HUDCall(examplezip, hudkey, 'zip')
g = czg.HUDCall(exampletract, hudkey, 'tract')

# Concatenate the output
print(pd.concat([h.pandas,g.pandas]))