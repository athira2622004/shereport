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

    # Build district summary data
    from collections import defaultdict
    district_data = defaultdict(lambda: {
        'total': 0, 'police': 0, 'anonymous': 0, 'crimes': defaultdict(int)
    })

    for r in requests:
        d = r.district
        if d not in DISTRICT_COORDS:
            continue
        district_data[d]['total'] += 1
        if r.reported_to_police:
            district_data[d]['police'] += 1
        if r.is_anonymous:
            district_data[d]['anonymous'] += 1
        crime_label = r.get_crime_type_display()
        district_data[d]['crimes'][crime_label] += 1

    # Build map pins — one per district
    district_pins = []
    for district, data in district_data.items():
        coords = DISTRICT_COORDS[district]
        crimes_sorted = sorted(
            data['crimes'].items(), key=lambda x: x[1], reverse=True)
        max_crime = crimes_sorted[0][1] if crimes_sorted else 1
        district_pins.append({
            'lat':       coords[0],
            'lng':       coords[1],
            'district':  district,
            'total':     data['total'],
            'police':    data['police'],
            'anonymous': data['anonymous'],
            'crimes':    crimes_sorted,
            'max_crime': max_crime,
        })

    total_count = sum(r['total'] for r in district_pins)
    police_reported = sum(r['police'] for r in district_pins)
    not_reported = total_count - police_reported
    anonymous_count = sum(r['anonymous'] for r in district_pins)

    from collections import Counter
    district_counts = {r['district']: r['total'] for r in district_pins}
    top_districts = sorted(district_counts.items(),
                           key=lambda x: x[1], reverse=True)[:5]
    max_district_count = top_districts[0][1] if top_districts else 1

    return render(request, 'data_insights/incident_map.html', {
        'district_pins_json': json.dumps(district_pins),
        'total_count':        total_count,
        'police_reported':    police_reported,
        'not_reported':       not_reported,
        'anonymous_count':    anonymous_count,
        'top_districts':      top_districts,
        'max_district_count': max_district_count,
        'crime_colors':       json.dumps(CRIME_COLORS),
    })
