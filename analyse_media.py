#!/usr/bin/env python

import pymediainfo
import os

def media_info(db_collection):

    for media_path in db_collection.distinct("full_path"):

        print(f'\n------\nFile analysed:\n{media_path}')

        from pymediainfo import MediaInfo
        media_info = MediaInfo.parse(media_path)

        if (len(list(media_info.tracks))) == 1:
            file_name = os.path.basename(media_path)
            print(f'--------------------\n!Warning! The following file does not have any track:\n{file_name}')
        else:
            audio_en, audio_fr, subs_en, subs_fr = ('no',)*4
            audio_status, subs_status =  ('blank',)*2

            for track in media_info.tracks:

                if track.track_type == 'Video':
                    resolution = track.height
                    video_codec = track.codec_id

                if track.track_type == 'Audio':
                    if track.language == 'en': audio_en = "yes"
                    if track.language == 'fr': audio_fr = "yes"

                if track.track_type == 'Text':
                    if track.language == 'en': subs_en = "yes"
                    if track.language == 'fr': subs_fr = "yes"

        if (audio_en == "yes" and audio_fr == "yes"): audio_status = 'green'
        elif (audio_en == "no" or audio_fr == "no"): audio_status = 'yellow'
        else: audio_status = 'red'

        if (subs_en == "yes" and subs_fr == "yes"): subs_status = 'green'
        elif (subs_en == "no" or subs_fr == "no"): subs_status = 'yellow'
        else: subs_status = 'red'

        media_dict = { "resolution": resolution, "video_codec": video_codec, "audio_en": audio_en, "audio_fr": audio_fr, "subs_en": subs_en, "subs_fr": subs_fr, "audio_status": audio_status, "subs_status": subs_status }

        db_collection.update({"full_path": media_path}, {"$set": (media_dict)})


if __name__ == "__main__":
    media_info(db_collection)
