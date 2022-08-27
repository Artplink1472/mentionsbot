import time
import telebot
import traceback
import config
import requests
import json
import logging
import copy
import asyncio
import aiohttp
import yarl
from aiohttp.helpers import quote
bot = telebot.TeleBot(config.token_bot)

bot.send_message(config.myid, '✅ Бот запущен')

logger = logging.getLogger('log')
logger.setLevel(logging.INFO)
formatstr = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(formatstr)

fh = logging.FileHandler('/home/tgbot/mentionsbot/log.log')
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
logger.addHandler(fh)


async def twitter_mentions(symbol, guest_token):
    mentions_count = 0
    global was_mentions, month
    try:
        async with app_storage['session'].get(yarl.URL(f"https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&include_ext_has_nft_avatar=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&include_ext_sensitive_media_warning=true&include_ext_trusted_friends_metadata=true&send_error_codes=true&simple_quoted_tweet=true&q=({quote(was_mentions[symbol]['Magic Eden']['twitter'])})%20-filter%3Areplies&tweet_search_mode=live&count=100&query_source=typed_query&pc=1&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel%2ChasNftAvatar%2CvoiceInfo%2Cenrichments%2CsuperFollowMetadata%2CunmentionInfo", encoded=True),
                                                        headers={'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA','x-guest-token': guest_token},
                                                        timeout=10) as mentionsrequest:
            mentionsresponse=await mentionsrequest.json(content_type=None)
            this_mentions_count=len(list(filter(lambda x: time.mktime(time.gmtime())-time.mktime(time.strptime(mentionsresponse['globalObjects']['tweets'][x]['created_at'][4:].replace(mentionsresponse['globalObjects']['tweets'][x]['created_at'][4:7],month.get(mentionsresponse['globalObjects']['tweets'][x]['created_at'][4:7])),"%m %d %H:%M:%S +0000 %Y"))<=86400, mentionsresponse['globalObjects']['tweets'])))
            mentions_count+=this_mentions_count
            cursor=mentionsresponse['timeline']['instructions'][0]['addEntries']['entries'][-1]['content']['operation']['cursor']['value']
        while len(mentionsresponse['globalObjects']['tweets'])-this_mentions_count<=1 and mentionsresponse['globalObjects']['tweets']:
            try:
                async with  app_storage['session'].get(yarl.URL(f"https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&include_ext_has_nft_avatar=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&include_ext_sensitive_media_warning=true&include_ext_trusted_friends_metadata=true&send_error_codes=true&simple_quoted_tweet=true&q=({quote(was_mentions[symbol]['Magic Eden']['twitter'])})%20-filter%3Areplies&tweet_search_mode=live&count=100&query_source=typed_query&cursor={quote(cursor)}&pc=1&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel%2ChasNftAvatar%2CvoiceInfo%2Cenrichments%2CsuperFollowMetadata%2CunmentionInfo", encoded=True),
                                                    headers={'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA','x-guest-token': guest_token},
                                                    timeout=10) as mentionsrequest:
                    mentionsresponse=await mentionsrequest.json(content_type=None)
                    this_mentions_count=len(list(filter(lambda x: time.mktime(time.gmtime())-time.mktime(time.strptime(mentionsresponse['globalObjects']['tweets'][x]['created_at'][4:].replace(mentionsresponse['globalObjects']['tweets'][x]['created_at'][4:7],month.get(mentionsresponse['globalObjects']['tweets'][x]['created_at'][4:7])),"%m %d %H:%M:%S +0000 %Y"))<=86400, mentionsresponse['globalObjects']['tweets'])))
                    mentions_count+=this_mentions_count
                    cursor=mentionsresponse['timeline']['instructions'][-1]['replaceEntry']['entry']['content']['operation']['cursor']['value']
            except Exception as e:
                logger.info(f'2 {e} ')
    except Exception as e:
        logger.info(f'twitter_mentions {e} {symbol}')
    logger.info(f'{symbol} {mentions_count}')
    return [symbol,mentions_count]

async def twitter_all_mentions(symbol, guest_token):
    mentions_count = 0
    try:
        async with app_storage['session'].get(yarl.URL(f'https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&include_ext_has_nft_avatar=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&include_ext_sensitive_media_warning=true&include_ext_trusted_friends_metadata=true&send_error_codes=true&simple_quoted_tweet=true&q=({quote(symbol)})&tweet_search_mode=live&count=100&query_source=typed_query&pc=1&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel%2ChasNftAvatar%2CvoiceInfo%2Cenrichments%2CsuperFollowMetadata%2CunmentionInfo', encoded=True),
                                                        headers={'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA','x-guest-token': guest_token},
                                                        timeout=10) as mentionsrequest:
            mentionsresponse = await mentionsrequest.json(content_type=None)
            mentions_count+=len(list(filter(lambda x: time.mktime(time.gmtime())-time.mktime(time.strptime(mentionsresponse['globalObjects']['tweets'][x]['created_at'][4:].replace(mentionsresponse['globalObjects']['tweets'][x]['created_at'][4:7],month.get(mentionsresponse['globalObjects']['tweets'][x]['created_at'][4:7])),"%m %d %H:%M:%S +0000 %Y"))<=86400 and symbol.lower() in mentionsresponse['globalObjects']['tweets'][x]['full_text'][mentionsresponse['globalObjects']['tweets'][x]['display_text_range'][0]:].lower(), mentionsresponse['globalObjects']['tweets'])))
            cursor=mentionsresponse['timeline']['instructions'][0]['addEntries']['entries'][-1]['content']['operation']['cursor']['value']
        try:
            while len(mentionsresponse['globalObjects']['tweets'])-len(list(filter(lambda x: time.mktime(time.gmtime())-time.mktime(time.strptime(mentionsresponse['globalObjects']['tweets'][x]['created_at'][4:].replace(mentionsresponse['globalObjects']['tweets'][x]['created_at'][4:7],month.get(mentionsresponse['globalObjects']['tweets'][x]['created_at'][4:7])),"%m %d %H:%M:%S +0000 %Y"))<=86400, mentionsresponse['globalObjects']['tweets'])))<=1 and mentionsresponse['globalObjects']['tweets']:
                try:
                    async with app_storage['session'].get(yarl.URL(f'https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&include_ext_has_nft_avatar=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&include_ext_sensitive_media_warning=true&include_ext_trusted_friends_metadata=true&send_error_codes=true&simple_quoted_tweet=true&q=({quote(symbol)})&tweet_search_mode=live&count=100&query_source=recent_search_click&cursor={quote(cursor)}&pc=1&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel%2ChasNftAvatar%2CvoiceInfo%2Cenrichments%2CsuperFollowMetadata%2CunmentionInfo', encoded=True),
                                                        headers={'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA','x-guest-token': guest_token},
                                                        timeout=10) as mentionsrequest:
                        mentionsresponse = await mentionsrequest.json(content_type=None)
                        mentions_count+=len(list(filter(lambda x: time.mktime(time.gmtime())-time.mktime(time.strptime(mentionsresponse['globalObjects']['tweets'][x]['created_at'][4:].replace(mentionsresponse['globalObjects']['tweets'][x]['created_at'][4:7],month.get(mentionsresponse['globalObjects']['tweets'][x]['created_at'][4:7])),"%m %d %H:%M:%S +0000 %Y"))<=86400 and symbol.lower() in mentionsresponse['globalObjects']['tweets'][x]['full_text'][mentionsresponse['globalObjects']['tweets'][x]['display_text_range'][0]:].lower(), mentionsresponse['globalObjects']['tweets'])))
                        cursor=mentionsresponse['timeline']['instructions'][-1]['replaceEntry']['entry']['content']['operation']['cursor']['value']
                except Exception as e:
                    logger.info(f'2 {e} {symbol}')
        except Exception as e:
            logger.info(f'!while! {e} {symbol} {mentionsresponse}')
    except Exception as e:
        logger.info(f'1 {e}')
    logger.info(f"{symbol} {mentions_count}")
    return [symbol, mentions_count]

async  def Magic_Eden_stats(symbol, proxy):
    Magic_Eden={'results': {}}
    try:
        if proxy:
            async with app_storage['session'].get(yarl.URL(f"https://api-mainnet.magiceden.dev/rpc/getCollectionEscrowStats/{symbol}", encoded=True),
                                                            proxy=proxy,
                                                            timeout=10) as mentionsrequest:
                Magic_Eden=await mentionsrequest.json(content_type=None)
        else:
            async with app_storage['session'].get(yarl.URL(f"https://api-mainnet.magiceden.dev/rpc/getCollectionEscrowStats/{symbol}", encoded=True),
                                                            timeout=10) as mentionsrequest:
                Magic_Eden=await mentionsrequest.json(content_type=None)
    except Exception as e:
        logger.info(f'Magic_Eden_stats {e} {symbol}')
    floorPrice,listedCount,volume24hr=Magic_Eden['results'].get('floorPrice'),Magic_Eden['results'].get('listedCount'),Magic_Eden['results'].get('volume24hr')
    return [symbol,(floorPrice if floorPrice else 0),(listedCount if listedCount else 0),(volume24hr if volume24hr else 0)]

app_storage={}
try:
    sended_12=[{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}]
    k=0
    f=0
    month={'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
    while True:
        sended_12.append(set())
        sended_all=set()
        for i in sended_12:
            sended_all.update(i)
        start_time=time.time()
        message=''
        message2='Список 2\n'
        message3 = 'Список 3\n'
        message4 = 'Список 4\n'
        with open('mentions.json', 'r') as f1:
            was_mentions=json.load(f1)
        new_collections=requests.get(f'https://api-mainnet.magiceden.dev/v2/collections?offset=0&limit=200').json()
        for collection in new_collections:
            try:
                if collection['symbol'] not in was_mentions and collection['twitter']:
                    was_mentions[collection['symbol']]={"Magic Eden": {"twitter": '@'+collection['twitter'][collection['twitter'].rfind('/')+1:], "floor": ['Just added','Just added','Just added','Just added','Just added','Just added','Just added','Just added','Just added','Just added','Just added','Just added','Just added','Just added','Just added','Just added','Just added','Just added','Just added','Just added','Just added','Just added','Just added','Just added'], "listedCount": ["Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added"], "volume24hr": ["Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added"], "image": collection.get('image')}, "mentions": ["Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added", "Just added"], "name": collection['name']}
            except Exception as e:
                bot.send_message(config.myid, f'{e} {collection}')
        mentions=copy.deepcopy(was_mentions)
        guest_token=requests.post('https://api.twitter.com/1.1/guest/activate.json',
                      headers={'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'}).json()['guest_token']
        async def start(was_mentions, guest_token):
            timeout = aiohttp.ClientTimeout(total=300)
            app_storage['session'] = aiohttp.ClientSession(timeout=timeout)
            async with app_storage['session']:
                tasks = []
                for symbol in was_mentions:
                    tasks.append(asyncio.create_task(twitter_mentions(symbol, guest_token)))
                results = await asyncio.gather(*tasks)
                for symbol in results:
                    mentions[symbol[0]]['mentions'].append(symbol[1])
        start_time2 = time.time()
        bot.send_message(config.myid, f'{start_time2}')
        asyncio.run(start(was_mentions, guest_token))
        logger.info(f'На выполнение прасинга ушло {time.time() - start_time2}')
        async def start3(was_mentions):
            timeout = aiohttp.ClientTimeout(total=300)
            app_storage['session'] = aiohttp.ClientSession(timeout=timeout)
            q=0
            async with app_storage['session']:
                tasks = []
                for symbol in was_mentions:
                    q+=1
                    if q%2:
                        tasks.append(asyncio.create_task(Magic_Eden_stats(symbol,False)))
                    else:
                        tasks.append(asyncio.create_task(Magic_Eden_stats(symbol,'http://51.89.191.227:10375')))
                    if q%238==0:
                        await asyncio.sleep(61)
                results = await asyncio.gather(*tasks)
                for symbol in results:
                    mentions[symbol[0]]['Magic Eden']['floor'].append(float(format(symbol[1]/1000000000,'.2f')))
                    mentions[symbol[0]]['Magic Eden']['listedCount'].append(symbol[2])
                    mentions[symbol[0]]['Magic Eden']['volume24hr'].append(float(format(symbol[3]/1000000000,'.2f')))
        start_time2 = time.time()
        bot.send_message(config.myid, f'{start_time2}')
        asyncio.run(start3(was_mentions))
        logger.info(f'На выполнение прасинга 3 ушло {time.time() - start_time2}')
        for symbol in was_mentions:
            if symbol not in sended_all:
                try:
                    if was_mentions[symbol]['Magic Eden']['floor'][0] != 'Just added' and mentions[symbol]['Magic Eden']['floor'][-1]/was_mentions[symbol]['Magic Eden']['floor'][0]>=1.1 and mentions[symbol]['mentions'][-1]/was_mentions[symbol]['mentions'][0] >= 1.5 and mentions[symbol]['mentions'][0] >= 10 and mentions[symbol]['Magic Eden']['listedCount'][-1]/mentions[symbol]['Magic Eden']['listedCount'][0]<=0.985:
                        message += f"{mentions[symbol]['name']} - Twitter mentions {was_mentions[symbol]['mentions'][0]}-->{mentions[symbol]['mentions'][-1]},\nfloor {was_mentions[symbol]['Magic Eden']['floor'][0]}-->{mentions[symbol]['Magic Eden']['floor'][-1]},\nlistedCount {was_mentions[symbol]['Magic Eden']['listedCount'][0]}-->{mentions[symbol]['Magic Eden']['listedCount'][-1]},\nSold24hr {was_mentions[symbol]['Magic Eden']['volume24hr'][0]}-->{mentions[symbol]['Magic Eden']['volume24hr'][-1]}\n"
                        sended_12[-1].add(symbol)
                except Exception as e:
                    logger.info(f'!!!!!!!!4 message {e}!!!!!!!!')
                try:
                    if was_mentions[symbol]['Magic Eden']['floor'][0] != 'Just added' and mentions[symbol]['Magic Eden']['listedCount'][-1]/mentions[symbol]['Magic Eden']['listedCount'][0]<=0.75 and mentions[symbol]['mentions'][0] >= 10:
                        message2 += f"{mentions[symbol]['name']} - Twitter mentions {was_mentions[symbol]['mentions'][0]}-->{mentions[symbol]['mentions'][-1]},\nfloor {was_mentions[symbol]['Magic Eden']['floor'][0]}-->{mentions[symbol]['Magic Eden']['floor'][-1]},\nlistedCount {was_mentions[symbol]['Magic Eden']['listedCount'][0]}-->{mentions[symbol]['Magic Eden']['listedCount'][-1]},\nSold24hr {was_mentions[symbol]['Magic Eden']['volume24hr'][0]}-->{mentions[symbol]['Magic Eden']['volume24hr'][-1]}\n"
                        sended_12[-1].add(symbol)
                except Exception as e:
                    logger.info(f'!!!!!!!!4 message {e}!!!!!!!!')
                try:
                    if was_mentions[symbol]['Magic Eden']['floor'][0] != 'Just added' and (mentions[symbol]['Magic Eden']['floor'][-1]/was_mentions[symbol]['Magic Eden']['floor'][0]-1)*100/(mentions[symbol]['mentions'][-1]-was_mentions[symbol]['mentions'][0])>=3 and mentions[symbol]['mentions'][-1] >= 10 and mentions[symbol]['mentions'][-1]-mentions[symbol]['mentions'][0] >= 6:
                        message3 += f"{mentions[symbol]['name']} - Twitter mentions {was_mentions[symbol]['mentions'][0]}-->{mentions[symbol]['mentions'][-1]},\nfloor {was_mentions[symbol]['Magic Eden']['floor'][0]}-->{mentions[symbol]['Magic Eden']['floor'][-1]},\nlistedCount {was_mentions[symbol]['Magic Eden']['listedCount'][0]}-->{mentions[symbol]['Magic Eden']['listedCount'][-1]},\nSold24hr {was_mentions[symbol]['Magic Eden']['volume24hr'][0]}-->{mentions[symbol]['Magic Eden']['volume24hr'][-1]}\n"
                        sended_12[-1].add(symbol)
                except Exception as e:
                    logger.info(f'!!!!!!!!4 message {e}!!!!!!!!')
                try:
                    if was_mentions[symbol]['Magic Eden']['floor'][0] != 'Just added' and (was_mentions[symbol]['Magic Eden']['floor'][-1]/was_mentions[symbol]['Magic Eden']['floor'][0]-1)*100/(mentions[symbol]['mentions'][-1]-was_mentions[symbol]['mentions'][0])>=3 and mentions[symbol]['mentions'][-1] >= 40 and mentions[symbol]['Magic Eden']['listedCount'][0] >= 50 and mentions[symbol]['mentions'][-1]-mentions[symbol]['mentions'][0] >= 6 and was_mentions[symbol]['Magic Eden']['volume24hr'][0]<was_mentions[symbol]['Magic Eden']['volume24hr'][-1] and was_mentions[symbol]['Magic Eden']['volume24hr'][-1]>=30:
                        message4 += f"{mentions[symbol]['name']} - Twitter mentions {was_mentions[symbol]['mentions'][0]}-->{mentions[symbol]['mentions'][-1]},\nfloor {was_mentions[symbol]['Magic Eden']['floor'][0]}-->{mentions[symbol]['Magic Eden']['floor'][-1]},\nlistedCount {was_mentions[symbol]['Magic Eden']['listedCount'][0]}-->{mentions[symbol]['Magic Eden']['listedCount'][-1]},\nSold24hr {was_mentions[symbol]['Magic Eden']['volume24hr'][0]}-->{mentions[symbol]['Magic Eden']['volume24hr'][-1]}\n"
                        sended_12[-1].add(symbol)
                except Exception as e:
                    logger.info(f'!!!!!!!!4 message {e}!!!!!!!!')
            mentions[symbol]['Magic Eden']['floor'],mentions[symbol]['Magic Eden']['listedCount'],mentions[symbol]['Magic Eden']['volume24hr'],mentions[symbol]['mentions'],sended_12=mentions[symbol]['Magic Eden']['floor'][-24:],mentions[symbol]['Magic Eden']['listedCount'][-24:],mentions[symbol]['Magic Eden']['volume24hr'][-24:],mentions[symbol]['mentions'][-24:],sended_12[-24:]
        while message:
            send = message[:message[:4096].rfind('\n') + 1]
            message = message[message[:4096].rfind('\n') + 1:]
            for user in config.rassilka:
                bot.send_message(user, send)
        while message2:
            send = message2[:message2[:4096].rfind('\n') + 1]
            message2 = message2[message2[:4096].rfind('\n') + 1:]
            for user in config.rassilka:
                bot.send_message(user, send)
        while message3:
            send = message3[:message3[:4096].rfind('\n') + 1]
            message3 = message3[message3[:4096].rfind('\n') + 1:]
            for user in config.rassilka:
                bot.send_message(user, send)
        while message4:
            send = message4[:message4[:4096].rfind('\n') + 1]
            message4 = message4[message4[:4096].rfind('\n') + 1:]
            for user in config.rassilka:
                bot.send_message(user, send)
        with open('mentions.json', 'w') as f1:
            json.dump(mentions, f1)
        mentions={}
        message = 'Топ 10\n'
        guest_token=requests.post('https://api.twitter.com/1.1/guest/activate.json',
                      headers={'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'}).json()['guest_token']
        async def start2(was_mentions, guest_token):
            timeout = aiohttp.ClientTimeout(total=300)
            app_storage['session'] = aiohttp.ClientSession(timeout=timeout)
            async with app_storage['session']:
                tasks = []
                for symbol in was_mentions:
                    tasks.append(asyncio.create_task(twitter_all_mentions(was_mentions[symbol]['Magic Eden']['twitter'], guest_token)))
                for twitter in ['@lonelylisteners','@zakironft','@satori_nft','@solswipecard','@dragonzlabz','@sentries_sol']:
                    tasks.append(asyncio.create_task(twitter_all_mentions(twitter, guest_token)))
                results = await asyncio.gather(*tasks)
                for symbol in results:
                    mentions[symbol[0]] = symbol[1]
        if k%48==0:
            start_time2 = time.time()
            bot.send_message(config.myid, f'{start_time2}')
            asyncio.run(start2(was_mentions, guest_token))
            logger.info(f'На выполнение прасинга 2 ушло {time.time() - start_time2}')
            for nickname in sorted(mentions, key=lambda x: mentions[x], reverse=True)[:10]:
                try:
                    message += f'{nickname} {mentions[nickname]}\n'
                except Exception as e:
                    logger.info(f'5 {e} {nickname}')
            for user in config.rassilka:
                bot.send_message(user, message)
        k+=1
        del mentions, was_mentions
        logger.info(f'Выполнение скрипта завершено {time.strftime("%m-%d-%Y %H:%M:%S",time.gmtime(time.time()))}')
        logger.info(f'Следующий запуск:{time.strftime("%m-%d-%Y %H:%M:%S",time.gmtime(start_time+1800))}')
        time.sleep(max(1800-(time.time()-start_time),0))
except:
    bot.send_message(config.myid, traceback.format_exc())
