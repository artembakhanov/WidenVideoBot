from libs.exception import VideoException
from libs.queue import start_video, stop_video
from libs.video import Video


def send_wide_video(bot, chat_id, video):
    """
    Send wide video from file.
    :param bot:
    :param chat_id:
    :param video:
    :return:
    """

    try:
        start_video(chat_id)
        video = Video(bot, video)
        bot.send_message(chat_id, f"⌛ Please, wait. It will take several seconds...")
        wide = video.make_wide()

        with open(wide, "rb") as file:
            bot.send_video(chat_id, file)

        video.remove_files()
    except VideoException as e:
        bot.send_message(chat_id, e.message)
    #except Exception as e:
    #    bot.send_message(chat_id, "😎 You send me something that could break me but I managed to stay alive. Try again")
    finally:
        stop_video(chat_id)
