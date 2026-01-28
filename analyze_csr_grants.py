#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تحليل بيانات CSR للشركات المصرية
Analysis of Egyptian Companies CSR Data for NGO Grant Opportunities
"""

import re
import json
from collections import defaultdict

def parse_kml_file(filename):
    """Parse KML file and extract company CSR information"""
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract all Placemark entries
    placemark_pattern = r'<Placemark>(.*?)</Placemark>'
    placemarks = re.findall(placemark_pattern, content, re.DOTALL)
    
    companies = []
    
    for placemark in placemarks:
        company = {}
        
        # Extract name
        name_match = re.search(r'<name>(.*?)</name>', placemark)
        if name_match:
            company['name'] = name_match.group(1)
        
        # Extract description details
        desc_match = re.search(r'<description><!\[CDATA\[(.*?)\]\]></description>', placemark, re.DOTALL)
        if desc_match:
            desc = desc_match.group(1)
            
            # Extract sector
            sector_match = re.search(r'<b>القطاع:</b>\s*(.*?)<br>', desc)
            if sector_match:
                company['sector'] = sector_match.group(1).strip()
            
            # Extract SDGs
            sdg_match = re.search(r'<b>SDGs:</b>\s*(.*?)<br>', desc)
            if sdg_match:
                company['sdgs'] = sdg_match.group(1).strip()
            
            # Extract governorates
            gov_match = re.search(r'<b>المحافظات:</b>\s*(.*?)<br>', desc)
            if gov_match:
                company['governorates'] = gov_match.group(1).strip()
            
            # Extract investment
            inv_match = re.search(r'<b>الاستثمار:</b>\s*(.*?)<br>', desc)
            if inv_match:
                company['investment'] = inv_match.group(1).strip()
            
            # Extract CSR type
            type_match = re.search(r'<b>نوع CSR:</b>\s*(.*?)(?:<br>|\r)', desc)
            if type_match:
                company['csr_type'] = type_match.group(1).strip()
            elif re.search(r'<b>النوع:</b>\s*(.*?)(?:<br>|\r)', desc):
                type_match = re.search(r'<b>النوع:</b>\s*(.*?)(?:<br>|\r)', desc)
                company['csr_type'] = type_match.group(1).strip()
            
            # Extract ESG Framework
            esg_match = re.search(r'<b>ESG Framework:</b>\s*(.*?)(?:<br>|\r)', desc)
            if esg_match:
                company['esg_framework'] = esg_match.group(1).strip()
            
            # Extract Impact Assessment
            impact_match = re.search(r'<b>تقييم الأثر:</b>\s*(.*?)(?:<br>|\r)', desc)
            if impact_match:
                company['impact_assessment'] = impact_match.group(1).strip()
        
        if company:
            companies.append(company)
    
    return companies

def analyze_grant_opportunities(companies):
    """Analyze which companies offer grants to NGOs"""
    
    grant_companies = []
    
    for company in companies:
        csr_type = company.get('csr_type', '')
        
        # Check if company offers grants
        if 'Grants' in csr_type or 'grants' in csr_type or 'منح' in csr_type:
            grant_companies.append(company)
    
    return grant_companies

def analyze_by_sector(companies):
    """Group companies by sector"""
    
    sectors = defaultdict(list)
    
    for company in companies:
        sector = company.get('sector', 'غير محدد')
        sectors[sector].append(company['name'])
    
    return dict(sectors)

def analyze_by_sdg(companies):
    """Analyze companies by SDG focus areas"""
    
    sdg_map = {
        '1': 'القضاء على الفقر',
        '2': 'القضاء على الجوع',
        '3': 'الصحة الجيدة والرفاه',
        '4': 'التعليم الجيد',
        '5': 'المساواة بين الجنسين',
        '6': 'المياه النظيفة والنظافة الصحية',
        '7': 'طاقة نظيفة وبأسعار معقولة',
        '8': 'العمل اللائق ونمو الاقتصاد',
        '9': 'الصناعة والابتكار والهياكل الأساسية',
        '10': 'الحد من أوجه عدم المساواة',
        '11': 'مدن ومجتمعات محلية مستدامة',
        '12': 'الاستهلاك والإنتاج المسؤولان',
        '13': 'العمل المناخي',
        '15': 'الحياة في البر',
        '17': 'عقد الشراكات لتحقيق الأهداف'
    }
    
    sdg_companies = defaultdict(list)
    
    for company in companies:
        sdgs = company.get('sdgs', '')
        if sdgs:
            sdg_list = [s.strip() for s in sdgs.split(',')]
            for sdg in sdg_list:
                if sdg in sdg_map:
                    sdg_companies[f"SDG {sdg}: {sdg_map[sdg]}"].append(company['name'])
    
    return dict(sdg_companies)

def generate_report(companies):
    """Generate comprehensive analysis report"""
    
    print("=" * 80)
    print("تحليل فرص المنح من الشركات المصرية للجمعيات غير الهادفة للربح")
    print("Analysis of Egyptian Companies CSR Grant Opportunities for NGOs")
    print("=" * 80)
    print()
    
    # Total companies
    print(f"📊 إجمالي الشركات المحللة: {len(companies)}")
    print(f"📊 Total Companies Analyzed: {len(companies)}")
    print()
    
    # Companies offering grants
    grant_companies = analyze_grant_opportunities(companies)
    print(f"💰 الشركات التي تقدم منح مباشرة: {len(grant_companies)}")
    print(f"💰 Companies Offering Direct Grants: {len(grant_companies)}")
    print()
    
    if grant_companies:
        print("الشركات التي تقدم منح:")
        print("Companies Offering Grants:")
        print("-" * 80)
        for i, company in enumerate(grant_companies, 1):
            print(f"{i}. {company['name']}")
            print(f"   القطاع: {company.get('sector', 'غير محدد')}")
            print(f"   نوع CSR: {company.get('csr_type', 'غير محدد')}")
            print(f"   الاستثمار: {company.get('investment', 'غير محدد')}")
            print(f"   أهداف التنمية المستدامة: {company.get('sdgs', 'غير محدد')}")
            print()
    
    # Analysis by sector
    print("=" * 80)
    print("📈 التحليل حسب القطاع")
    print("📈 Analysis by Sector")
    print("=" * 80)
    sectors = analyze_by_sector(companies)
    for sector, company_list in sorted(sectors.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"\n{sector}: {len(company_list)} شركة")
        for company in company_list[:5]:  # Show top 5
            print(f"  • {company}")
        if len(company_list) > 5:
            print(f"  ... و {len(company_list) - 5} شركة أخرى")
    
    # Analysis by SDG
    print("\n" + "=" * 80)
    print("🎯 التحليل حسب أهداف التنمية المستدامة (SDGs)")
    print("🎯 Analysis by Sustainable Development Goals (SDGs)")
    print("=" * 80)
    sdg_companies = analyze_by_sdg(companies)
    for sdg, company_list in sorted(sdg_companies.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
        print(f"\n{sdg}: {len(company_list)} شركة")
        for company in company_list[:3]:  # Show top 3
            print(f"  • {company}")
        if len(company_list) > 3:
            print(f"  ... و {len(company_list) - 3} شركة أخرى")
    
    # Investment analysis
    print("\n" + "=" * 80)
    print("💵 تحليل الاستثمار")
    print("💵 Investment Analysis")
    print("=" * 80)
    
    high_investment = []
    for company in companies:
        investment = company.get('investment', '')
        if any(indicator in investment for indicator in ['>100', 'مليار', 'billion', '$1']):
            high_investment.append({
                'name': company['name'],
                'investment': investment,
                'sector': company.get('sector', 'غير محدد')
            })
    
    print(f"\nالشركات ذات الاستثمار الأعلى في CSR:")
    print(f"Companies with Highest CSR Investment:")
    for i, company in enumerate(high_investment[:10], 1):
        print(f"{i}. {company['name']}")
        print(f"   القطاع: {company['sector']}")
        print(f"   الاستثمار: {company['investment']}")
        print()
    
    # ESG Framework analysis
    print("=" * 80)
    print("🌱 تحليل إطار ESG")
    print("🌱 ESG Framework Analysis")
    print("=" * 80)
    
    esg_companies = [c for c in companies if c.get('esg_framework') == 'نعم']
    print(f"\nالشركات التي لديها إطار ESG: {len(esg_companies)}")
    print(f"Companies with ESG Framework: {len(esg_companies)}")
    print()
    
    # Impact assessment analysis
    impact_companies = [c for c in companies if c.get('impact_assessment') == 'نعم']
    print(f"الشركات التي تقوم بتقييم الأثر: {len(impact_companies)}")
    print(f"Companies with Impact Assessment: {len(impact_companies)}")
    print()
    
    # Recommendations
    print("=" * 80)
    print("💡 توصيات للجمعيات غير الهادفة للربح")
    print("💡 Recommendations for NGOs")
    print("=" * 80)
    print("""
1. استهدف الشركات التي تقدم منح مباشرة (Grants):
   Target companies offering direct grants:
   • فودافون مصر (Vodafone Egypt)
   • أورنج مصر (Orange Egypt)
   • مايكروسوفت مصر (Microsoft Egypt)

2. ركز على القطاعات ذات الاستثمار الأعلى:
   Focus on sectors with highest investment:
   • البنوك (Banking)
   • الاتصالات (Telecommunications)
   • الطاقة (Energy)

3. وافق مشاريعك مع أهداف التنمية المستدامة الأكثر شيوعاً:
   Align projects with most common SDGs:
   • SDG 4: التعليم الجيد (Quality Education)
   • SDG 3: الصحة الجيدة (Good Health)
   • SDG 13: العمل المناخي (Climate Action)
   • SDG 8: العمل اللائق (Decent Work)

4. استهدف الشركات التي لديها إطار ESG وتقييم أثر:
   Target companies with ESG framework and impact assessment
   (أكثر احتمالاً للتمويل المستدام)
   (More likely for sustainable funding)

5. قم ببناء علاقات طويلة الأمد:
   Build long-term relationships:
   • احضر فعاليات CSR
   • تواصل مع مسؤولي الاستدامة
   • أظهر تأثير مشاريعك السابقة
    """)
    
    print("=" * 80)
    print("تم إنشاء التقرير بنجاح!")
    print("Report Generated Successfully!")
    print("=" * 80)
    
    # Save detailed data to JSON
    output_data = {
        'total_companies': len(companies),
        'grant_companies': len(grant_companies),
        'grant_company_details': grant_companies,
        'sectors': sectors,
        'sdg_analysis': sdg_companies,
        'high_investment_companies': high_investment,
        'esg_companies_count': len(esg_companies),
        'impact_assessment_companies_count': len(impact_companies)
    }
    
    with open('csr_grants_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print("\n📁 تم حفظ البيانات التفصيلية في: csr_grants_analysis.json")
    print("📁 Detailed data saved to: csr_grants_analysis.json")

if __name__ == "__main__":
    # Parse KML file
    print("جاري تحليل البيانات...")
    print("Analyzing data...")
    print()
    
    companies = parse_kml_file('CSR_Egypt_50_Companies.kml')
    
    # Generate report
    generate_report(companies)
