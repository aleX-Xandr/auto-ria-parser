import asyncio

from components.worker import MainWorker

async def main() -> None:
    worker = MainWorker()
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())





# import requests

# cookies = {
#     'Path': '/',
#     'chk': '1',
#     '__utma': '79960839.414505191.1717407109.1717407109.1717407109.1',
#     '__utmc': '79960839',
#     '__utmz': '79960839.1717407109.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
#     '__utmb': '79960839.2.10.1717407109',
#     '_ga': 'GA1.1.962960160.1717407111',
#     '_gcl_au': '1.1.275174289.1717407111',
#     'Path': '/',
#     '_fbp': 'fb.1.1717407113791.1742510685',
#     'test_new_features': '442',
#     'advanced_search_test': '42',
#     'promolink2': '1',
#     'showNewFeatures': '7',
#     '_504c2': 'http://10.42.19.107:3000',
#     'FCCDCF': '%5Bnull%2Cnull%2Cnull%2C%5B%22CP_oksAP_oksAEsACBRUA3EgAAAAAEPgAAggAAAOhQD2F2K2kKFkPCmQWYAQBCijYEAhQAAAAkCBIAAgAUgQAgFIIAgAIFAAAAAAAAAQEgCQAAQABAAAIACgAAAAAAIAAAAAAAQQAAAAAIAAAAAAAAEAAAAAAAQAAAAIAABEhCAAQQAEAAAAAAAQAAAAAAAAAAABAAA%22%2C%222~~dv.70.89.93.108.122.149.196.259.311.313.323.358.415.449.486.494.495.540.574.609.827.864.981.1029.1048.1051.1095.1097.1126.1205.1211.1276.1301.1365.1415.1423.1449.1570.1577.1598.1651.1716.1735.1753.1765.1870.1878.1889.1958.2072.2253.2299.2357.2373.2415.2506.2526.2568.2571.2575.2624.2677%22%2C%2225216E86-3C29-427B-B224-667894EFD1AF%22%5D%5D',
#     '__eoi': 'ID=473b0df805d5edb2:T=1717407221:RT=1717407221:S=AA-AfjZjnTYH0BcOD8oS4YEiLMix',
#     '_ga_KGL740D7XD': 'GS1.1.1717407110.1.1.1717407231.56.0.1762085934',
# }

# headers = {
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#     'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
#     'cache-control': 'no-cache',
#     # 'cookie': 'Path=/; chk=1; __utma=79960839.414505191.1717407109.1717407109.1717407109.1; __utmc=79960839; __utmz=79960839.1717407109.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmb=79960839.2.10.1717407109; _ga=GA1.1.962960160.1717407111; _gcl_au=1.1.275174289.1717407111; Path=/; _fbp=fb.1.1717407113791.1742510685; test_new_features=442; advanced_search_test=42; promolink2=1; showNewFeatures=7; _504c2=http://10.42.19.107:3000; FCCDCF=%5Bnull%2Cnull%2Cnull%2C%5B%22CP_oksAP_oksAEsACBRUA3EgAAAAAEPgAAggAAAOhQD2F2K2kKFkPCmQWYAQBCijYEAhQAAAAkCBIAAgAUgQAgFIIAgAIFAAAAAAAAAQEgCQAAQABAAAIACgAAAAAAIAAAAAAAQQAAAAAIAAAAAAAAEAAAAAAAQAAAAIAABEhCAAQQAEAAAAAAAQAAAAAAAAAAABAAA%22%2C%222~~dv.70.89.93.108.122.149.196.259.311.313.323.358.415.449.486.494.495.540.574.609.827.864.981.1029.1048.1051.1095.1097.1126.1205.1211.1276.1301.1365.1415.1423.1449.1570.1577.1598.1651.1716.1735.1753.1765.1870.1878.1889.1958.2072.2253.2299.2357.2373.2415.2506.2526.2568.2571.2575.2624.2677%22%2C%2225216E86-3C29-427B-B224-667894EFD1AF%22%5D%5D; __eoi=ID=473b0df805d5edb2:T=1717407221:RT=1717407221:S=AA-AfjZjnTYH0BcOD8oS4YEiLMix; _ga_KGL740D7XD=GS1.1.1717407110.1.1.1717407231.56.0.1762085934',
#     'pragma': 'no-cache',
#     'priority': 'u=0, i',
#     'referer': 'https://auto.ria.com/',
#     'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-fetch-dest': 'document',
#     'sec-fetch-mode': 'navigate',
#     'sec-fetch-site': 'same-origin',
#     'sec-fetch-user': '?1',
#     'upgrade-insecure-requests': '1',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
# }

# params = {
#     'indexName': 'auto',
#     'size': '20',
# }

# response = requests.get('https://auto.ria.com/api/search/auto', params=params, cookies=cookies, headers=headers)
# print(response.text)

# '{"additional_params":{"lang_id":2,"page":0,"view_type_id":0,"target":"search","section":"auto","catalog_name":"","elastica":true,"nodejs":true,"searchByTypeAction":true},"result":{"search_result":{"ids":["36690172","36549938","36689333","36683713","36468437","36685439","36642682","36669417","36676435","35603849"],"count":348089,"last_id":0},"search_result_common":{"count":348089,"last_id":0,"data":[{"id":"36690172","type":"UsedAuto"},{"id":"36549938","type":"UsedAuto"},{"id":"100500","type":"OfferOfTheDay"},{"id":"36689333","type":"UsedAuto"},{"id":"36683713","type":"UsedAuto"},{"id":"36468437","type":"UsedAuto"},{"id":"36685439","type":"UsedAuto"},{"id":"36642682","type":"UsedAuto"},{"id":"36669417","type":"UsedAuto"},{"id":"36676435","type":"UsedAuto"},{"id":"35603849","type":"UsedAuto"}]},"active_marka":null,"active_model":null,"active_state":null,"active_city":null,"revies":null,"isCommonSearch":false,"additional":{"user_auto_positions":[],"search_params":{"all":{"indexName":"auto","size":"20","searchType":2,"target":"search","event":"little","lang_id":2,"page":0,"limit_page":null,"countpage":10,"last_id":0,"saledParam":0,"marka_id":[],"model_id":[],"mm_marka_filtr":[],"mm_model_filtr":[],"useOrigAutoTable":false,"withoutStatus":false,"with_photo":false,"with_video":false,"under_credit":0,"confiscated_car":0,"exchange_filter":[],"old_only":false,"auto_options":[],"user_id":[],"person_id":0,"with_discount":false,"auto_id_str":"","black_user_id":0,"order_by":0,"is_online":false,"withoutCache":false,"with_last_id":false,"top":0,"currency":1,"currency_id":0,"currencies_arr":[],"power_name":0,"powerFrom":0,"powerTo":0,"hide_black_list":[],"custom":0,"abroad":false,"damage":0,"star_auto":0,"price_ot":0,"price_do":0,"s_yers":[null],"po_yers":[null],"year":0,"auto_ids_search_position":0,"print_qs":0,"is_hot":0,"deletedAutoSearch":0,"can_be_checked":0,"excludeMM":[],"generation_id":[],"modification_id":[]},"cleaned":{"indexName":"auto","size":"20","searchType":2,"target":"search","event":"little","lang_id":2,"countpage":10,"marka_id":[],"model_id":[],"mm_marka_filtr":[],"mm_model_filtr":[],"exchange_filter":[],"auto_options":[],"user_id":[],"currency":1,"currencies_arr":[],"hide_black_list":[],"s_yers":[null],"po_yers":[null],"excludeMM":[],"generation_id":[],"modification_id":[]}},"query_string":"indexName=auto&size=20"}}}'