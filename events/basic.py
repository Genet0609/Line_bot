from line_bot_api import *

def about_us_event(event):

    emoji = [

        {
            "index" : 0,
            "productId": "5ac2213e040ab15980c9b447",
            "emojiId" :"085"
        },

        {
            "index" : 1,
            "productId": "5ac21c4e031a6752fb806d5b",
            "emojiId" :"039"
        },
        {
            "index" : 2,
            "productId": "5ac21c4e031a6752fb806d5b",
            "emojiId" :"052"
        },

        {
            "index" : 3,
            "productId": "5ac21c4e031a6752fb806d5b",
            "emojiId" :"012"
        },

        {
            "index" : 4,
            "productId": "5ac21c4e031a6752fb806d5b",
            "emojiId" :"053"
        },

        {
            "index" : 5,
            "productId": "5ac21c4e031a6752fb806d5b",
            "emojiId" :"161"
        },

        {
            "index" : 6,
            "productId": "5ac21c4e031a6752fb806d5b",
            "emojiId" :"014"
        },

        {
            "index" : 7,
            "productId": "5ac21c4e031a6752fb806d5b",
            "emojiId" :"161"
        },
        {
            "index" : 8,
            "productId": "5ac2213e040ab15980c9b447",
            "emojiId" :"085"
        },

    ]

    text_message = TextSendMessage(text="""$$$$$$$$$ 
哈囉！你好哇！恭喜你已經成為了莉飄兒大人的部下！""",emojis=emoji)
    
    sticker_message = StickerSendMessage(
        package_id="11537",
        sticker_id="52002748"
    )
    line_bot_api.reply_message(
        event.reply_token,
        [text_message,sticker_message]
    )