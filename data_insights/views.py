from django.shortcuts import render
from core.models import CrimeStatistic, DistrictData
from support.models import SupportRequest
import json


def data_insights(request):
    stats = list(CrimeStatistic.objects.all().order_by('year'))

    years = [s.year for s in stats]
    totals = [s.total_crimes for s in stats]

    # Always use the LATEST year for crime type breakdown
    latest_year = stats[-1].year if stats else 'N/A'
    crime_labels = ['Rape', 'Molestation', 'Kidnapping',
                    'Cruelty by Husband', 'Dowry Deaths', 'Harassment', 'Other']
    if stats:
        latest = stats[-1]
        crime_values = [latest.rape, latest.molestation, latest.kidnapping,
                        latest.cruelty_by_husband, latest.dowry_deaths,
                        latest.harassment, latest.other]
    else:
        crime_values = [0] * 7

    # District data — use latest year available in district table
    latest_district_year = DistrictData.objects.order_by(
        '-year').values_list('year', flat=True).first()
    if latest_district_year:
        districts = list(DistrictData.objects.filter(
            year=latest_district_year).order_by('-total_crimes'))
    else:
        districts = []

    district_names = [d.district for d in districts]
    district_totals = [d.total_crimes for d in districts]
    map_data = {d.district: d.total_crimes for d in districts}

    context = {
        'stats':               stats,
        'chart_years':         json.dumps(years),
        'chart_totals':        json.dumps(totals),
        'crime_labels':        json.dumps(crime_labels),
        'crime_values':        json.dumps(crime_values),
        'latest_year':         latest_year,
        'districts':           districts,
        'latest_district_year': latest_district_year or 'N/A',
        'district_names':      json.dumps(district_names),
        'district_totals':     json.dumps(district_totals),
        'map_data':            json.dumps(map_data),
        'has_district_data':   len(districts) > 0,
    }
    return render(request, 'data_insights/data_insights.html', context)


def incident_map(request):
    """Live incident pin map from support requests."""
    import random
    DISTRICT_COORDS = {
        'Thiruvananthapuram': [8.5241, 76.9366],
        'Kollam':             [8.8932, 76.6141],
        'Pathanamthitta':     [9.2648, 76.7870],
        'Alappuzha':          [9.4981, 76.3388],
        'Kottayam':           [9.5916, 76.5222],
        'Idukki':             [9.9189, 77.1025],
        'Ernakulam':          [10.0159, 76.3419],
        'Thrissur':           [10.5276, 76.2144],
        'Palakkad':           [10.7867, 76.6548],
        'Malappuram':         [11.0730, 76.0740],
        'Kozhikode':          [11.2588, 75.7804],
        'Wayanad':            [11.6854, 76.1320],
        'Kannur':             [11.8745, 75.3704],
        'Kasaragod':          [12.4996, 74.9869],
    }
    CRIME_COLORS = {
        'domestic_violence': '#E8401A',
        'rape':              '#7B2D8B',
        'molestation':       '#185FA5',
        'stalking':          '#BA7517',
        'kidnapping':        '#444441',
        'dowry':             '#993C1D',
        'trafficking':       '#0F6E56',
        'workplace':         '#3B6D11',
        'other':             '#888780',
    }
    requests = SupportRequest.objects.filter(
        district__isnull=False).exclude(district='')
    incidents = []
    for r in requests:
        coords = DISTRICT_COORDS.get(r.district)
        if not coords:
            continue
        lat = coords[0] + random.uniform(-0.05, 0.05)
        lng = coords[1] + random.uniform(-0.05, 0.05)
        incidents.append({
            'lat':      round(lat, 4),
            'lng':      round(lng, 4),
            'district': r.district,
            'type':     r.crime_type,
            'label':    r.get_crime_type_display(),
            'color':    CRIME_COLORS.get(r.crime_type, '#888780'),
            'month':    r.created_at.strftime('%B %Y'),
            'police':   'Yes' if r.reported_to_police else 'No',
        })
    return render(request, 'data_insights/incident_map.html', {
        'incidents_json': json.dumps(incidents),
        'total_count':    len(incidents),
        'crime_colors':   json.dumps(CRIME_COLORS),
    })
