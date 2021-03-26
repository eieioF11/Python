from line_notify_bot import LINENotifyBot

def main():
    bot = LINENotifyBot(access_token='UilHhgEr7klUFPxhWyHdxYrJDbomRgXxLWeeNJsFyqY')
    bot.send(message="hellow world!")
    bot.send(
        message="Test!",
        #image='images.png',  # png or jpg
        sticker_package_id=1,#スタンプ
        sticker_id=1,#id 1 1~17
        )


if __name__ == "__main__":
    main()