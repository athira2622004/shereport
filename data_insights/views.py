from django.shortcuts import render
from core.models import CrimeStatistic, DistrictData
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
