import pandas as pd
import hud_geo as czg

with open('config/hudkey','r') as o:
    hudkey = o.read()

examplezip = '75031'
exampletract = '48113010801'

h = czg.HUDCall(examplezip, hudkey, 'zip')
g = czg.HUDCall(exampletract, hudkey, 'tract')
