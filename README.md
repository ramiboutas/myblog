# myblog
This a Wagtail blog created by @ramiboutas



# To do:

* promote panels (instagram / fb / telegram):
  * Promote, boolean field (promote? Yes or no)
  * Datetime field to schedule post publishing (default one hour after the page_published signal)
  * optional field (if filled out: use this, if not use self.title for caption/ post description)

* set up celery

* set up signals depending on topics and page instance language
  * topics: settings.SOCIAL_MEDIA_PROMOTING_CHOICES
  * language: page.locale.language_code

```Python
HOW TO USE THIS
>>> from django.conf import settings
>>> accounts = settings.INSTAGRAM_ACCOUNTS
>>> accounts
{'es': {'API_PUBLIC': 'whatever ES', 'USERNAME': 'whatever ES'}, 'en': {'API_PUBLIC': 'whatever EN', 'USERNAME': 'whatever EN'}, 'de': {'API_PUBLIC': 'whatever DE', 'USERNAME': 'whatever DE'}}
>>> accounts["en"]
{'API_PUBLIC': 'whatever EN', 'USERNAME': 'whatever EN'}
>>> accounts["en"]["API_PUBLIC"]
'whatever EN'

if "page" is a Page instance, we can get its language code:
page.locale.language_code
```



* Auto promoting page instances in instagram (3 accounts es, en, de): auto generate images from page instance titles and post it through the API

* Auto promoting in facebook (3 pages es, en, de): post it through the API, https://developers.facebook.com/docs/pages/publishing/


* Auto promoting in telegram (3 channel es, en, de): auto generate images from page instance titles and post it through the API https://medium.com/javarevisited/sending-a-message-to-a-telegram-channel-the-easy-way-eb0a0b32968


* Auto promoting in linkedin (use my profile): post it through the API https://medium.com/@9cv9official/understanding-apis-and-using-linkedins-api-to-make-a-post-1563cb3b0064

* check for more tasks to do :)
