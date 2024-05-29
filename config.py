pixel_vars = ['Qrvr', 'Qlat']
shed_vars = ['Def', 'EA', 'EB', 'ESUM', 'GwDep',
             'Pcp', 'QQA', 'QQG', 'QQS',
             'SnHgt', 'SnWE', 'SoilFrstDep', 'SoilMoist', 'SoilThawDep',
             'SubOutQ', 'SubSurfWtrDep', 'Tair']

vars_long_names = {
    'Qrvr': 'water_volume_transport_in_river_channel',
    'Qlat': 'incoming_water_volume_transport_along_river_channel',
    'Def': 'water_vapor_saturation_deficit_in_air',
    'EA': 'water_evaporation_amount_from_horizon_a',
    'EB': 'water_evaporation_amount_from_horizon_b',
    'ESUM': 'total_water_evaporation_amount',
    'GwDep': '',
    'Pcp': 'precipitation_amount',
    'QQA': '',
    'QQG': '',
    'QQS': '',
    'SnHgt': 'surface_snow_thickness',
    'SnWE': 'surface_snow_amount',
    'SoilFrstDep': 'depth_at_base_of_frozen_ground',
    'SoilMoist': 'volume_fraction_of_condensed_water_in_soil_at_field_capacity',
    'SoilThawDep': 'depth_at_top_of_frozen_ground',
    'SubOutQ': 'water_volume_transport_in_river_channel',
    'SubSurfWtrDep': '',
    'Tair': 'air_temperature'
}

vars_units = {
    'Qrvr': 'm3 s-1',
    'Qlat': 'm3 s-1',
    'Def': 'Pa',
    'EA': 'kg m-2',
    'EB': 'kg m-2',
    'ESUM': 'kg m-2',
    'GwDep': 'm',
    'Pcp': 'kg m-2',
    'QQA': 'm3 s-1',
    'QQG': 'm3 s-1',
    'QQS': 'm3 s-1',
    'SnHgt': 'cm',
    'SnWE': 'kg m-2',
    'SoilFrstDep': 'm',
    'SoilMoist': '',
    'SoilThawDep': 'm',
    'SubOutQ': 'm3 s-1',
    'SubSurfWtrDep': '',
    'Tair': 'K'
}
