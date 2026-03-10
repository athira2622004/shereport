from django.shortcuts import render, get_object_or_404
from .models import CrimeStatistic, NewsUpdate


def home(request):
    try:
        stats = list(CrimeStatistic.objects.all().order_by('year'))
    except Exception:
        stats = []
    try:
        news = NewsUpdate.objects.filter(is_active=True)[:4]
    except Exception:
        news = []

    chart_years = [s.year for s in stats]
    chart_totals = [s.total_crimes for s in stats]

    context = {
        'stats':        stats,
        'news':         news,
        'chart_years':  chart_years,
        'chart_totals': chart_totals,
        'has_data':     len(stats) > 0,
        'latest_year':  stats[-1].year if stats else 'N/A',
        'latest_total': stats[-1].total_crimes if stats else 0,
    }
    return render(request, 'core/home.html', context)


def about(request):
    objectives = [
        "Curate and systematise data on crimes from news, police & judicial sources",
        "Provide accessible, guided reporting and legal literacy support to survivors",
        "Facilitate coordination among police, legal aid, counsellors, media and academia",
        "Build sustained public awareness on consent, reporting, and allyship",
        "Generate evidence-based insights for policy reform and institutional accountability",
        "Ensure that victims are not subjected to re-victimisation",
        "Create a feedback loop between ground realities and state-level policy making",
    ]
    return render(request, 'core/about.html', {'objectives': objectives})


def what_is_she_report(request):
    return render(request, 'core/what_is_she_report.html')


def news_detail(request, pk):
    item = get_object_or_404(NewsUpdate, pk=pk, is_active=True)
    recent = NewsUpdate.objects.filter(is_active=True).exclude(pk=pk)[:3]
    return render(request, 'core/news_detail.html', {'item': item, 'recent': recent})
