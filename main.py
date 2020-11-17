from video_processor.processor import VideoProcessor
from detector.reference import Reference
from detector import detector
from cv2 import imread, imshow, waitKey
from GUI.navigator import Navigator
from GUI.sub_pages.hero_select import HeroSelect
from GUI.sub_pages.item_suggestions import ItemSuggestions
from GUI.hero import Hero
from threading import Thread
from time import sleep
import random


def listen_for_stop_detection(item_suggestions, video_processor):
    while not video_processor.force_stop:
        sleep(1)
        if not item_suggestions.is_active and video_processor.is_running:
            video_processor.force_stop = True


def listen_for_detection(navigator):
    sub_pages = navigator.get_sub_pages()
    item_suggestions = [x for x in sub_pages if type(x) is ItemSuggestions][0]

    video_processor = VideoProcessor('assets/videos/replays/sample_test.mov')
    video_processor.frame_before_callback = 30  # for debugging

    while True:
        if item_suggestions.is_active and item_suggestions.last_hero is not None \
                and not video_processor.is_running:
            args = {'page': item_suggestions, 'references': []}
            for item_image in item_suggestions.last_hero.item_images_ref:
                color = (int(random.uniform(0, 256)), int(random.uniform(0, 256)), int(random.uniform(0, 256)))
                args['references'].append(Reference(imread(item_image), 0, 0, 0, 0, color))

            t = Thread(target=listen_for_stop_detection, args=(item_suggestions, video_processor))
            t.start()

            video_processor.run(detector.frame_check, detector.after_frame_check, args)
        else:
            sleep(1)


if __name__ == '__main__':

    prefix = "assets/images/items/"
    items = ["chainmail.png", "crown.png", "belt_of_strength.png", "quelling_blade.png", "boots_of_speed.png", "ogre_axe.png"]
    item_refs = ["aaaa3.png", "aaaa2.png", "aaaa.png", "aaaa5.png", "aaaa6.png", "aaaa7.png"]
    for i in range(0, len(items)):
        items[i] = prefix + items[i]
        item_refs[i] = prefix + item_refs[i]

    under_lord = Hero('assets/images/heroes/underlord.png', items, item_refs)
    anti_mage = Hero('assets/images/heroes/anti_mage.png', items, item_refs)
    shadow_shaman = Hero('assets/images/heroes/shadow_shaman.png', items, item_refs)

    heroes = [under_lord, anti_mage, shadow_shaman]

    n = Navigator(HeroSelect, heroes)

    thread = Thread(target=listen_for_detection, args=(n,))
    thread.start()

    n.run()





