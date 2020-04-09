import requests
import csv

access_token = FB_ACCESS_TOKEN
search_page_ids = ['105732052794210',  # DUP
                   '111956985487415',  # SDLP
                   '10642639740']  # Alliance
ads = 2500


def query_ad_library(token, page_ids, total_ads):
    # Initialise two csv files for response data
    mf_cols = ['id', 'ad_creation_time', 'ad_creative_body', 'ad_creative_link_caption',
               'ad_creative_link_description', 'ad_creative_link_title', 'ad_delivery_start_time',
               'ad_delivery_stop_time', 'ad_snapshot_url', 'currency', 'funding_entity', 'page_id',
               'page_name', 'impression_range', 'spend_range', 'platforms']
    master_file = open('data.csv', 'w')
    mf_writer = csv.DictWriter(master_file, fieldnames=mf_cols, extrasaction='ignore')
    mf_writer.writeheader()

    demo_cols = ['id', 'age', 'gender', 'percentage']
    demographics_file = open('demos_data.csv', 'w')
    demo_writer = csv.DictWriter(demographics_file, fieldnames=demo_cols, extrasaction='ignore')
    demo_writer.writeheader()

    # Loop through page_ids provided and write response to csv files
    fields = ['id', 'ad_creation_time', 'ad_creative_body', 'ad_creative_link_caption',
              'ad_creative_link_description', 'ad_creative_link_title', 'ad_delivery_start_time',
              'ad_delivery_stop_time', 'ad_snapshot_url', 'currency', 'demographic_distribution',
              'funding_entity', 'impressions', 'page_id', 'page_name', 'publisher_platforms',
              'region_distribution', 'spend']

    payload = {'access_token': token,
               'ad_reached_countries': 'GB',
               'ad_type': 'POLITICAL_AND_ISSUE_ADS',
               'fields': ','.join(fields),
               'ad_active_status': 'ALL',
               'search_page_ids': '',
               'limit': total_ads}

    for search_page_id in page_ids:
        payload.update(search_page_ids=search_page_id)
        r = requests.get('https://graph.facebook.com/v6.0/ads_archive', params=payload)
        response = r.json()
        for ad in response['data']:
            ad['impression_range'] = ','.join(ad['impressions'].values())
            ad['spend_range'] = ','.join(ad['spend'].values())
            ad['platforms'] = ','.join(ad['publisher_platforms'])
            mf_writer.writerow(ad)

            for ad_demo in ad['demographic_distribution']:
                ad_demo.update(id=ad['id'])
            demo_writer.writerows(ad['demographic_distribution'])

    master_file.close()
    demographics_file.close()
    return


if __name__ == '__main__':
    query_ad_library(access_token, search_page_ids, ads)
