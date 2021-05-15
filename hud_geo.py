import requests
import pandas as pd
import json

# Assumes you've gotten a HUD census key at ./config/hudkey 
# from https://www.huduser.gov/hudapi/public/register?comingfrom=1
# Supports Zip->Tract or Tract->Zip

request_url = 'https://www.huduser.gov/hudapi/public/register?comingfrom=1'

class HUDCall():
    def __init__(
        self,
        geo_value: str,
        hud_apikey : str,
        geotype : str
    ):
        self.geotype = geotype
        self.geo_value = geo_value
        self.request = self.call_api(hud_apikey)
        print(self.request.status_code)
        if self.request.status_code ==200:
            self.json = json.loads(self.request.text)
            self.pandas = self._toPandas()
        else:
            RuntimeError(f'Request invalid. Status code {self.request.status_code} received.')
            
    def help(self):
        '''Tag to keep crosswalks straight'''
        print(f'General info: Queries HUD API with available key registered from {request_url}')
        if self.geotype =='zip':
            print('Using zip-tract crosswalk:','Identifies what proportion of a zipcode lies across census tracts.',
                sep='\n\t')
        if self.geotype =='tract':
            print('Using tract-zip crosswalk:','Identifies what proportion of a tract lies within a zipcode.',
                sep='\n\t')
        print('For more information, please see https://www.huduser.gov/portal/dataset/uspszip-api.html')
        

    def call_api(self,apikey ):
        baseurl = 'https://www.huduser.gov/hudapi/public/usps'
        if self.geotype == 'zip': _type = 1
        elif self.geotype =='tract': _type = 6
        if (len(self.geo_value) != 5 and _type ==1):
            raise ValueError('Only 5 digit zipcode supported. Check input.')
        elif (len(self.geo_value) !=11 and _type==6):
            raise ValueError('Census tracts are 11 digits. Check input.')
            
        call = baseurl + f'?type={_type}&query={self.geo_value}'
        request_header =  {'Authorization': f'Bearer {apikey}'}
        r = requests.get(call, headers=request_header)
        return r

    def _toPandas(self):
        j = self.json['data']
        _tuple = (
            (   j['year'], j['quarter'], j['input'], j['crosswalk_type'], self.geotype,
                j['results'][n]['geoid']) for n, _ in enumerate(j['results']))
        _dict = {}
        for n, t in enumerate(_tuple):
            tmp_val = j['results'][n]
            _dict[t] = {x:tmp_val[x] for x in tmp_val.keys() if 'ratio' in x}
        df = pd.DataFrame.from_dict(_dict, orient='index')
        df.index.set_names(
            ['year','quarter','input_value','crosswalk_type','geotype','crosswalk_value'], 
            inplace=True)
        return df
